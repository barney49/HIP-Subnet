(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{7362:function(e,t,r){Promise.resolve().then(r.bind(r,8315))},8315:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return j}});var s=r(7437),n=r(2265),a=r(9143),i=r(7742),l=r(3167),o=r(1367);function c(){for(var e=arguments.length,t=Array(e),r=0;r<e;r++)t[r]=arguments[r];return(0,o.m6)((0,l.W)(t))}let d=(0,i.j)("inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),u=n.forwardRef((e,t)=>{let{className:r,variant:n,size:i,asChild:l=!1,...o}=e,u=l?a.g7:"button";return(0,s.jsx)(u,{className:c(d({variant:n,size:i,className:r})),ref:t,...o})});u.displayName="Button";var f=r(4602);let m=(0,i.j)("text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"),h=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(f.f,{ref:t,className:c(m(),r),...n})});h.displayName=f.f.displayName;var x=r(5628),g=r(7019);let p=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(x.fC,{className:c("grid gap-2",r),...n,ref:t})});p.displayName=x.fC.displayName;let b=n.forwardRef((e,t)=>{let{className:r,...n}=e;return(0,s.jsx)(x.ck,{ref:t,className:c("aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",r),...n,children:(0,s.jsx)(x.z$,{className:"flex items-center justify-center",children:(0,s.jsx)(g.Z,{className:"h-2.5 w-2.5 fill-current text-current"})})})});function y(e){var t;let{task:r,onSubmit:a,submitting:i}=e,[l,o]=(0,n.useState)(null),[c,d]=(0,n.useState)("");return(0,n.useEffect)(()=>{o(r.options?r.options[0]:null),d("")},[r]),(0,s.jsxs)("div",{className:"flex flex-col md:flex-row h-screen",children:[(0,s.jsxs)("div",{className:"md:w-1/2 md:p-4 flex flex-col items-center justify-center bg-yellow-200 p-8 overflow-y-scroll",children:[r.image&&(0,s.jsx)("img",{src:r.image,alt:"image associated with the task",className:"rounded-lg mb-4 w-full md:w-auto"}),(0,s.jsx)("p",{children:r.value})]}),(0,s.jsxs)("div",{className:"md:w-1/2 bg-white p-8 flex flex-col items-center md:items-start justify-center",children:[(0,s.jsx)("h2",{className:"text-xl font-bold mb-4 text-center md:text-left",children:r.label}),"select"===r.type?(0,s.jsx)(p,{value:null!=l?l:void 0,onValueChange:e=>{o(e)},children:null===(t=r.options)||void 0===t?void 0:t.map((e,t)=>(0,s.jsxs)("div",{className:"flex items-center space-x-2",children:[(0,s.jsx)(b,{value:e,id:e}),(0,s.jsx)(h,{htmlFor:e,children:e})]},t))}):(0,s.jsx)("input",{type:"text",value:c,onChange:e=>d(e.target.value),className:"border-2 border-gray-300 p-2 rounded-md"}),(0,s.jsx)("div",{className:"mt-4",children:(0,s.jsx)(u,{onClick:()=>{"select"===r.type&&null!==l?a(l,r.id):"text"===r.type&&""!==c&&a(c,r.id)},disabled:i||"select"===r.type&&null===l||"text"===r.type&&""===c,children:i?"Submitting...":"Submit"})})]})]})}async function v(){try{let e=await fetch("/api/tasks",{cache:"no-store"});if(!e.ok)throw Error("Failed to fetch tasks");return await e.json()}catch(e){throw console.error("Error fetching tasks:",e),e}}async function w(e,t){try{if(!(await fetch("/api/answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({answer:e,id:t})})).ok)throw Error("Failed to submit answer")}catch(e){throw console.error("Error submitting answer:",e),e}}function j(){let[e,t]=(0,n.useState)([]),[r,a]=(0,n.useState)(!0),[i,l]=(0,n.useState)(null),[o,c]=(0,n.useState)(!1);(0,n.useEffect)(()=>{let e=async()=>{try{let e=await v();t(e),!i&&e.length>0&&l(e[0])}catch(e){console.error("Error fetching tasks:",e)}finally{a(!1)}};e();let r=setInterval(e,5e3);return()=>{clearInterval(r)}},[i]);let d=async(t,r)=>{if(!o){c(!0);try{await w(t,r);let s=e.findIndex(e=>e.id===(null==i?void 0:i.id)),n=e[s+1]||null;l(n)}catch(e){console.error("Error submitting answer:",e)}finally{c(!1)}}};return(0,s.jsx)(s.Fragment,{children:i?(0,s.jsx)(y,{task:i,onSubmit:d,submitting:o}):(0,s.jsx)("div",{className:"flex h-screen w-full row text-center align-middle justify-center items-center",children:(0,s.jsx)("h1",{className:"text-4xl font-bold text-slate-800",children:r?"Loading...":"No tasks available at the moment. Please wait."})})})}b.displayName=x.ck.displayName}},function(e){e.O(0,[529,971,69,744],function(){return e(e.s=7362)}),_N_E=e.O()}]);