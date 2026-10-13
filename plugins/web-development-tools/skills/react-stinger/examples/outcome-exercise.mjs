// Synthetic pure behavior exercise. No React mount, Vite build or network.
import assert from 'node:assert/strict';
const beforeView = s => ({name:s.name.trim(), selected:s.items.filter(x=>x.selected).map(x=>x.id), canSave:!s.pending&&s.name.trim().length>0});
const selectIds = items => items.filter(x=>x.selected).map(x=>x.id);
const afterView = s => ({name:s.name.trim(), selected:selectIds(s.items), canSave:!s.pending&&s.name.trim().length>0});
const samples=[{name:' Alice ',pending:false,items:[{id:'a',selected:true},{id:'b',selected:false}]},{name:' ',pending:false,items:[]},{name:'Draft',pending:true,items:[{id:'b',selected:true}]}];
for(const state of samples) assert.deepEqual(beforeView(state),afterView(state));
function reducer(state,event){
 switch(event.type){
 case 'start':return {...state,request:event.id,pending:true,error:null};
 case 'success':return event.id===state.request?{...state,pending:false,data:event.data}:state;
 case 'failure':return event.id===state.request?{...state,pending:false,error:event.error}:state;
 case 'dispose':return {...state,request:null,pending:false};
 default:return state;
 }
}
let s={request:null,pending:false,data:[],error:null};
s=reducer(s,{type:'start',id:'A'});s=reducer(s,{type:'start',id:'B'});
s=reducer(s,{type:'success',id:'B',data:['B']});const current=s;
s=reducer(s,{type:'success',id:'A',data:['A']});assert.strictEqual(s,current);
assert.deepEqual(s.data,['B']);assert.equal(s.pending,false);
s=reducer(s,{type:'start',id:'C'});s=reducer(s,{type:'dispose'});
assert.strictEqual(reducer(s,{type:'success',id:'C',data:['C']}),s);
s=reducer(s,{type:'start',id:'D'});s=reducer(s,{type:'failure',id:'D',error:'unavailable'});assert.equal(s.error,'unavailable');assert.equal(s.pending,false);
const initial={request:null,pending:false,data:[],error:null};reducer(initial,{type:'start',id:'A'});assert.deepEqual(initial,{request:null,pending:false,data:[],error:null});
console.log(JSON.stringify({verdict:'PASS',selectorComparisons:3,requestCases:['obsolete response','pending completion','dispose invalidation','active rejection','pure original state'],limits:'Pure JS only; no mounted React, Strict Mode, transport cancellation or UI equivalence.'},null,2));
