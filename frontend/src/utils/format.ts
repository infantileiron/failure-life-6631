export const decimal=(v:number|null,d=3)=>v===null?'不可估计':v.toFixed(d);export const median=(v:number|null)=>v===null?'未达到':v+' h';export const percent=(v:number)=>(v*100).toFixed(1)+'%';
