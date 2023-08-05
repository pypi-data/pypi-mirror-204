"use strict";(self.webpackChunkmitosheet3=self.webpackChunkmitosheet3||[]).push([[827,833],{827:(e,t,o)=>{o.r(t),o.d(t,{default:()=>g});var n=o(33),i=o(123);const l=new(o(502).LabIcon)({name:"mitosheet:mitosheet-jlab-icon",svgstr:'<svg width="7" height="11" viewBox="0 0 7 11" fill="none" xmlns="http://www.w3.org/2000/svg">    <rect x="0.871094" y="2.87109" width="5.52567" height="5.3994" fill="#D0B9FE"/>    <ellipse cx="3.63393" cy="2.80053" rx="2.76283" ry="2.0603" fill="#D0B9FE"/>    <ellipse cx="3.63393" cy="8.20092" rx="2.76283" ry="2.0603" fill="#D0B9FE"/>    <path d="M0.871094 2.94922H3.2966C3.57827 2.94922 3.80661 3.17755 3.80661 3.45922V3.45922C3.80661 3.74088 3.57827 3.96922 3.29661 3.96922H0.871094V2.94922Z" fill="#9D6CFF"/>    <path d="M0.871094 7.03125H3.2966C3.57827 7.03125 3.80661 7.25958 3.80661 7.54125V7.54125C3.80661 7.82292 3.57827 8.05125 3.29661 8.05125H0.871094V7.03125Z" fill="#9D6CFF"/>    <path d="M6.39673 4.99023H3.97122C3.68955 4.99023 3.46122 5.21857 3.46122 5.50023V5.50023C3.46122 5.7819 3.68955 6.01023 3.97122 6.01023H6.39673V4.99023Z" fill="#9D6CFF"/>    </svg>'}),s={1:"from mitosheet.public.v1 import *",2:"from mitosheet.public.v2 import *",3:"from mitosheet.public.v3 import *"};function a(e){const t=e.split(/\r?\n/).filter((e=>e.trim().length>0));return t.length>0?t.pop():void 0}function r(e){const t=a(e);return void 0!==t&&-1!==t.indexOf("sheet(")}function c(e,t){const o=e.replace(/\s/g,"");return o.includes("sheet(")&&o.includes(`analysis_to_replay="${t}"`)}function d(e){const t=e.replace(/\s/g,"");return r(e)&&t.includes("analysis_to_replay=")}function m(){let e=document.activeElement;for(;null!==e&&!e.classList.contains("mito-container");)e=e.parentElement;return e}function u(e,t){if(null==e)return;const o=e.iter();let n=o.next(),i=0;for(;n;){if(i==t)return n;i++,n=o.next()}}function h(e){return null==e?"":e.modelDB.get("value").text}function v(e){return void 0!==e&&""===h(e).trim()}function f(e,t){var o,n;const i=null===(o=e.currentWidget)||void 0===o?void 0:o.content,l=null===(n=null==i?void 0:i.model)||void 0===n?void 0:n.cells;if(void 0===l)return;const s=l.iter();let a=s.next(),r=0;for(;a;){if(c(h(a),t))return[a,r];r++,a=s.next()}}function y(e,t){var o,n,i;if(t){const o=f(e,t);if(void 0!==o)return o}const l=null===(o=e.currentWidget)||void 0===o?void 0:o.content,s=null===(n=null==l?void 0:l.model)||void 0===n?void 0:n.cells;if(null==l||null==s)return;const a=null===(i=l.activeCell)||void 0===i?void 0:i.model,c=l.activeCellIndex,m=u(s,c-1);if(m&&r(h(m))&&!d(h(m)))return[m,c-1];if(a&&r(h(a))&&!d(h(a)))return[a,c];let v=c;for(;v>=0;){const e=u(s,v);if(e&&r(h(e))&&!d(h(e)))return[e,v];v--}}function p(e,t){null!=e&&(e.modelDB.get("value").text=t)}const g={id:"mitosheet:plugin",requires:[i.INotebookTracker],activate:function(e,t){(e=>{e.widgetAdded.connect(((e,t)=>{const o=new n.ToolbarButton({className:"toolbar-mito-button-class",icon:l,onClick:()=>{var e;null===(e=window.commands)||void 0===e||e.execute("mitosheet:create-empty-mitosheet")},tooltip:"Create a blank Mitosheet below the active code cell",label:"New Mitosheet"});t.toolbar.insertAfter("cellType","Create Mito Button",o)}))})(t),e.commands.addCommand("mitosheet:create-mitosheet-comm",{label:"Create Comm",execute:async e=>{var o,n;const i=e.kernelID,l=e.commTargetID,s=t.find((e=>{var t,o;return(null===(o=null===(t=e.sessionContext.session)||void 0===t?void 0:t.kernel)||void 0===o?void 0:o.id)===i})),a=null===(n=null===(o=null==s?void 0:s.sessionContext)||void 0===o?void 0:o.session)||void 0===n?void 0:n.kernel;return null==a?"no_backend_comm_registered_error":a.createComm(l)}}),e.commands.addCommand("mitosheet:write-analysis-to-replay-to-mitosheet-call",{label:"Given an analysisName, writes it to the mitosheet.sheet() call that created this mitosheet, if it is not already written to this cell.",execute:e=>{const o=e.analysisName,n=e.mitoAPI,i=y(t,o);if(i){const[e]=i,t=function(e,t){if(r(h(e))&&!d(h(e))){const o=h(e),n=o.lastIndexOf(")");let i="";return i=o.includes("sheet()")?`analysis_to_replay="${t}")`:`, analysis_to_replay="${t}")`,p(e,o.substring(0,n)+i+o.substring(n+1)),!0}return!1}(e,o);if(t)return}n.log("write_analysis_to_replay_to_mitosheet_call_failed")}}),e.commands.addCommand("mitosheet:overwrite-analysis-to-replay-to-mitosheet-call",{label:"Given an oldAnalysisName and newAnalysisName, writes the newAnalysisName to the mitosheet.sheet() call that has the oldAnalysisName.",execute:e=>{const o=e.oldAnalysisName,n=e.newAnalysisName,i=e.mitoAPI,l=f(t,o);if(void 0===l)return;const[s]=l,a=function(e,t,o){return!(!r(h(e))||!c(h(e),t))&&(p(e,h(e).replace(RegExp(`analysis_to_replay\\s*=\\s*"${t}"`),`analysis_to_replay="${o}"`)),!0)}(s,o,n);a||i.log("overwrite_analysis_to_replay_to_mitosheet_call_failed")}}),e.commands.addCommand("mitosheet:write-generated-code-cell",{label:"Writes the generated code for a mito analysis to the cell below the mitosheet.sheet() call that generated this analysis. NOTE: this should only be called after the analysis_to_replay has been written in the mitosheet.sheet() call, so this cell can be found correctly.",execute:e=>{var o,n,l;const a=e.analysisName,r=function(e,t,o,n){if(0==t.length)return"";let i="";if(t.length>0)for(let e=0;e<t.length;e++)(l=t[e]).startsWith("#")&&-1===l.indexOf("\n")&&(i+="\n"),i+=t[e]+"\n";var l;const a=s[n];return o?`${a}; register_analysis("${e}");\n${i}`:`${a}; # Analysis Name:${e};\n${i}`}(a,e.code,e.telemetryEnabled,e.publicInterfaceVersion),c=f(t,a);if(void 0===c)return;const[,d]=c,m=null===(o=t.currentWidget)||void 0===o?void 0:o.content,y=null===(n=null==m?void 0:m.model)||void 0===n?void 0:n.cells;if(void 0===m||void 0===y)return;const g=m.activeCellIndex,b=u(y,d+1);if(v(b)||function(e,t){return function(e){let t=!1;return Object.values(s).forEach((o=>{(e.startsWith(o+"; register_analysis(")||e.startsWith(o+"; # Analysis Name:"))&&(t=!0)})),e.startsWith("# MITO CODE START")||e.startsWith("from mitosheet import *; register_analysis(")||e.startsWith("from mitosheet import *; # Analysis:")||e.startsWith("from mitosheet import *; # Analysis Name:")||t}(e)&&e.includes(t)}(h(b),a))p(b,r);else{if(d!==g)if(d<g)for(let e=0;e<g-d;e++)i.NotebookActions.selectAbove(m);else if(d>g)for(let e=0;e<d-g;e++)i.NotebookActions.selectBelow(m);i.NotebookActions.insertBelow(m),p(null===(l=null==m?void 0:m.activeCell)||void 0===l?void 0:l.model,r)}}}),e.commands.addCommand("mitosheet:write-code-snippet-cell",{label:"Writes the generated code for a mito analysis to the cell below the mitosheet.sheet() call that generated this analysis. NOTE: this should only be called after the analysis_to_replay has been written in the mitosheet.sheet() call, so this cell can be found correctly.",execute:e=>{var o,n,l;const s=e.analysisName,a=e.code,r=f(t,s);if(void 0===r)return;const[,c]=r,d=null===(o=t.currentWidget)||void 0===o?void 0:o.content,m=null===(n=null==d?void 0:d.model)||void 0===n?void 0:n.cells;if(void 0===d||void 0===m)return;const h=u(m,c+2);v(h)?p(h,a):(i.NotebookActions.selectBelow(d),i.NotebookActions.insertBelow(d),p(null===(l=null==d?void 0:d.activeCell)||void 0===l?void 0:l.model,a))}}),e.commands.addCommand("mitosheet:get-args",{label:"Reads the arguments passed to the mitosheet.sheet call.",execute:e=>{const o=e.analysisToReplayName,n=y(t,o);if(n){const[e]=n;return(e=>{let t=e.split("sheet(")[1].split(")")[0];t.includes("analysis_to_replay")&&(t=t.split("analysis_to_replay")[0].trim()),t.includes("view_df")&&(t=t.split("view_df")[0].trim());let o=t.split(",").map((e=>e.trim()));return o=o.filter((e=>e.length>0)),o})(h(e))}return[]}}),e.commands.addCommand("mitosheet:create-mitosheet-from-dataframe-output",{label:"creates a new mitosheet from the dataframe that is printed",execute:async()=>{var e,o,n;const l=null===(e=t.currentWidget)||void 0===e?void 0:e.content,s=null===(o=t.currentWidget)||void 0===o?void 0:o.context;if(!l||!s)return;let r=a(h(null===(n=l.activeCell)||void 0===n?void 0:n.model));(null==r?void 0:r.endsWith(".head()"))&&(r=r.split(".head()")[0]),i.NotebookActions.clearOutputs(l),i.NotebookActions.insertBelow(l);const c=l.activeCell;p(null==c?void 0:c.model,`import mitosheet\nmitosheet.sheet(${r})`),i.NotebookActions.run(l,s.sessionContext)}}),e.commands.addCommand("mitosheet:create-empty-mitosheet",{label:"Creates a new empty mitosheet",execute:async()=>{var e,o;const n=null===(e=t.currentWidget)||void 0===e?void 0:e.content,l=null===(o=t.currentWidget)||void 0===o?void 0:o.context;if(!n||!l)return;i.NotebookActions.insertBelow(n);const s=n.activeCell;p(null==s?void 0:s.model,"import mitosheet\nmitosheet.sheet()"),i.NotebookActions.run(n,l.sessionContext)}}),e.commands.addKeyBinding({command:"mitosheet:focus-on-search",args:{},keys:["Accel F"],selector:".mito-container"}),e.commands.addCommand("mitosheet:focus-on-search",{label:"Focuses on search of the currently selected mito notebook",execute:async()=>{const e=m(),t=null==e?void 0:e.querySelector("#action-search-bar-id");null==t||t.focus()}}),e.commands.addKeyBinding({command:"mitosheet:mito-undo",args:{},keys:["Accel Z"],selector:".mito-container"}),e.commands.addCommand("mitosheet:mito-undo",{label:"Clicks the undo button once",execute:async()=>{var e,t;const o=m();if("input"===(null===(e=document.activeElement)||void 0===e?void 0:e.tagName.toLowerCase())||"textarea"===(null===(t=document.activeElement)||void 0===t?void 0:t.tagName.toLowerCase()))return;const n=null==o?void 0:o.querySelector("#mito-undo-button");null==n||n.click()}}),e.commands.addKeyBinding({command:"mitosheet:mito-redo",args:{},keys:["Accel Y"],selector:".mito-container"}),e.commands.addCommand("mitosheet:mito-redo",{label:"Clicks the redo button once",execute:async()=>{var e,t;const o=m();if("input"===(null===(e=document.activeElement)||void 0===e?void 0:e.tagName.toLowerCase())||"textarea"===(null===(t=document.activeElement)||void 0===t?void 0:t.tagName.toLowerCase()))return;const n=null==o?void 0:o.querySelector("#mito-redo-button");null==n||n.click()}}),e.commands.addKeyBinding({command:"mitosheet:do-nothing",args:{},keys:["Shift Enter"],selector:".mito-container"}),e.commands.addCommand("mitosheet:do-nothing",{label:"Does nothing",execute:async()=>{}}),window.commands=e.commands},autoStart:!0}}}]);