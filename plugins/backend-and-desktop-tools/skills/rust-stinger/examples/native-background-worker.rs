#![forbid(unsafe_code)]
use std::io::{Cursor, Read};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, mpsc};
use std::thread::{self, JoinHandle};

#[derive(Debug, PartialEq, Eq)]
enum Outcome {
    Complete(u64),
    Cancelled,
    InvalidInput,
    Overflow,
}
#[derive(Debug, PartialEq, Eq)]
struct Job {
    id: u8,
    value: u64,
    malformed: bool,
}
#[derive(Debug, PartialEq, Eq)]
enum Admission {
    Full(Job),
    Closed(Job),
    LifetimeLimit(Job),
}
#[derive(Debug, PartialEq, Eq)]
enum ShutdownError {
    Panicked,
}

// Memory-only reader stands in for a fallible blocking boundary, not real file I/O.
fn execute(job: &Job, cancel: &AtomicBool) -> Outcome {
    execute_with_checkpoint(job, cancel, |_| {})
}

// Hook models cancellation arriving at a known compute boundary without sleeps.
fn execute_with_checkpoint(
    job: &Job,
    cancel: &AtomicBool,
    mut checkpoint: impl FnMut(u8),
) -> Outcome {
    if cancel.load(Ordering::Acquire) {
        return Outcome::Cancelled;
    }
    let bytes = job.value.to_le_bytes();
    let mut reader = Cursor::new(if job.malformed {
        &bytes[..3]
    } else {
        &bytes[..]
    });
    let mut decoded = [0; 8];
    if reader.read_exact(&mut decoded).is_err() {
        return Outcome::InvalidInput;
    }
    let value = u64::from_le_bytes(decoded);
    let mut total = 0_u64;
    for chunk in 0..4 {
        checkpoint(chunk);
        if cancel.load(Ordering::Acquire) {
            return Outcome::Cancelled;
        }
        match total.checked_add(value) {
            Some(next) => total = next,
            None => return Outcome::Overflow,
        }
    }
    Outcome::Complete(total)
}

struct Worker {
    admission: Option<mpsc::SyncSender<Job>>,
    cancel: Arc<AtomicBool>,
    handle: JoinHandle<Vec<(u8, Outcome)>>,
    accepted: u8,
}
impl Worker {
    fn start(gate: mpsc::Receiver<()>) -> Self {
        let (tx, rx) = mpsc::sync_channel::<Job>(1);
        let cancel = Arc::new(AtomicBool::new(false));
        let observed_cancel = Arc::clone(&cancel);
        let handle = thread::spawn(move || {
            // Test gate resolves by send OR disconnect before shutdown joins.
            let _ = gate.recv();
            let mut outcomes = Vec::with_capacity(2);
            for job in rx {
                outcomes.push((job.id, execute(&job, &observed_cancel)));
            }
            outcomes
        });
        Self {
            admission: Some(tx),
            cancel,
            handle,
            accepted: 0,
        }
    }
    fn submit(&mut self, job: Job) -> Result<(), Admission> {
        let Some(tx) = self.admission.as_ref() else {
            return Err(Admission::Closed(job));
        };
        if self.accepted == 2 {
            return Err(Admission::LifetimeLimit(job));
        }
        match tx.try_send(job) {
            Ok(()) => {
                self.accepted += 1;
                Ok(())
            }
            Err(mpsc::TrySendError::Full(job)) => Err(Admission::Full(job)),
            Err(mpsc::TrySendError::Disconnected(job)) => Err(Admission::Closed(job)),
        }
    }
    fn close_admission(&mut self) {
        self.admission.take();
    }
    fn request_cancel(&self) {
        self.cancel.store(true, Ordering::Release);
    }
    fn shutdown(mut self) -> Result<Vec<(u8, Outcome)>, ShutdownError> {
        self.close_admission();
        self.handle.join().map_err(|_| ShutdownError::Panicked)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn job(id: u8, value: u64) -> Job {
        Job {
            id,
            value,
            malformed: false,
        }
    }
    fn gated() -> (mpsc::Sender<()>, Worker) {
        let (tx, rx) = mpsc::channel();
        (tx, Worker::start(rx))
    }
    #[test]
    fn success_is_joined_and_correlated() {
        let (gate, mut worker) = gated();
        assert_eq!(worker.submit(job(7, 12)), Ok(()));
        gate.send(()).unwrap();
        assert_eq!(worker.shutdown(), Ok(vec![(7, Outcome::Complete(48))]));
    }
    #[test]
    fn full_queue_returns_ownership_of_rejected_job() {
        let (gate, mut worker) = gated();
        worker.submit(job(1, 2)).unwrap();
        assert_eq!(worker.submit(job(2, 3)), Err(Admission::Full(job(2, 3))));
        drop(gate);
        assert_eq!(worker.shutdown(), Ok(vec![(1, Outcome::Complete(8))]));
    }
    #[test]
    fn cancellation_before_start_is_terminal_not_success() {
        let (gate, mut worker) = gated();
        worker.submit(job(9, 100)).unwrap();
        worker.request_cancel();
        gate.send(()).unwrap();
        assert_eq!(worker.shutdown(), Ok(vec![(9, Outcome::Cancelled)]));
    }
    #[test]
    fn malformed_reader_error_survives_join() {
        let (gate, mut worker) = gated();
        worker
            .submit(Job {
                id: 3,
                value: 99,
                malformed: true,
            })
            .unwrap();
        drop(gate);
        assert_eq!(worker.shutdown(), Ok(vec![(3, Outcome::InvalidInput)]));
    }
    #[test]
    fn overflow_is_domain_error_not_panic() {
        let (gate, mut worker) = gated();
        worker.submit(job(4, u64::MAX)).unwrap();
        drop(gate);
        assert_eq!(worker.shutdown(), Ok(vec![(4, Outcome::Overflow)]));
    }
    #[test]
    fn admission_closed_rejects_job_and_shutdown_joins_empty_worker() {
        let (gate, mut worker) = gated();
        worker.close_admission();
        assert_eq!(worker.submit(job(5, 1)), Err(Admission::Closed(job(5, 1))));
        drop(gate);
        assert_eq!(worker.shutdown(), Ok(vec![]));
    }
    #[test]
    fn lifetime_bound_preserves_job_ownership() {
        let (gate, mut worker) = gated();
        // Counter branch is independent of scheduling; no extra jobs accepted.
        worker.accepted = 2;
        assert_eq!(
            worker.submit(job(6, 1)),
            Err(Admission::LifetimeLimit(job(6, 1)))
        );
        drop(gate);
        assert_eq!(worker.shutdown(), Ok(vec![]));
    }
    #[test]
    fn cancellation_between_compute_chunks_discards_partial_result() {
        let cancel = AtomicBool::new(false);
        let mut visited = Vec::new();
        let result = execute_with_checkpoint(&job(8, 10), &cancel, |chunk| {
            visited.push(chunk);
            if chunk == 2 {
                cancel.store(true, Ordering::Release);
            }
        });
        assert_eq!(visited, vec![0, 1, 2]);
        assert_eq!(result, Outcome::Cancelled);
    }
    #[test]
    fn thread_panic_becomes_typed_shutdown_error() {
        let handle = thread::spawn(|| panic!("synthetic-worker-failure"));
        let worker = Worker {
            admission: None,
            cancel: Arc::new(AtomicBool::new(false)),
            handle,
            accepted: 0,
        };
        assert_eq!(worker.shutdown(), Err(ShutdownError::Panicked));
    }
    #[test]
    fn cancelled_compute_has_no_partial_complete_result() {
        let cancel = AtomicBool::new(true);
        assert_eq!(execute(&job(8, u64::MAX), &cancel), Outcome::Cancelled);
    }
}
