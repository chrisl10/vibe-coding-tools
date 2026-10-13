'use strict';
const { runBuilder } = require('./render-case-document');
if (require.main === module) {
  runBuilder('pre_litigation').catch(error => {
    process.stderr.write(`Case document refused: ${error.message}\n`);
    process.exitCode = 1;
  });
}
module.exports = { run: argv => runBuilder('pre_litigation', argv) };
