(function(t){function e(e){for(var a,r,i=e[0],l=e[1],c=e[2],u=0,f=[];u<i.length;u++)r=i[u],Object.prototype.hasOwnProperty.call(s,r)&&s[r]&&f.push(s[r][0]),s[r]=0;for(a in l)Object.prototype.hasOwnProperty.call(l,a)&&(t[a]=l[a]);d&&d(e);while(f.length)f.shift()();return o.push.apply(o,c||[]),n()}function n(){for(var t,e=0;e<o.length;e++){for(var n=o[e],a=!0,i=1;i<n.length;i++){var l=n[i];0!==s[l]&&(a=!1)}a&&(o.splice(e--,1),t=r(r.s=n[0]))}return t}var a={},s={app:0},o=[];function r(e){if(a[e])return a[e].exports;var n=a[e]={i:e,l:!1,exports:{}};return t[e].call(n.exports,n,n.exports,r),n.l=!0,n.exports}r.m=t,r.c=a,r.d=function(t,e,n){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},r.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)r.d(n,a,function(e){return t[e]}.bind(null,a));return n},r.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="/vesting_dashboard/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],l=i.push.bind(i);i.push=e,i=i.slice();for(var c=0;c<i.length;c++)e(i[c]);var d=l;o.push([0,"chunk-vendors"]),n()})({0:function(t,e,n){t.exports=n("56d7")},"0673":function(t,e,n){"use strict";n("6018")},"20f8":function(t,e,n){},"56d7":function(t,e,n){"use strict";n.r(e);var a=n("2b0e"),s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-main",[a("v-container",{staticClass:"my-5"},[a("h2",[t._v("TFT Vesting Portal")]),a("v-img",{staticClass:"mx-auto mb-12 mt-12",attrs:{"lazy-src":n("da3f"),height:"auto",width:"250",src:n("da3f")}}),a("Overview",{staticClass:"mb-16"}),a("h3",[t._v("© 2021 "),a("a",{attrs:{href:"https://new.threefold.io",target:"blank"}},[t._v("ThreeFold Foundation")]),t._v(". All rights reserved.")])],1)],1)],1)},o=[],r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("VestingForm",{attrs:{getVestingInfo:t.getVestingInfo,setLoading:t.setLoading}}),n("AccountTable",{attrs:{vestinginfo:t.vestinginfo,loading:t.loading}})],1)},i=[],l=n("bc3a"),c=n.n(l),d=c.a.create({baseURL:"/vesting_dashboard/api",withCredentials:!0,headers:{Accept:"application/json","Content-Type":"application/json","Access-Control-Allow-Origin":"*"}}),u={createAccount:function(t){return d.post("/account/create",{owner_address:t})},listAccounts:function(){return d.get("/account/list")}},f=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-form",{ref:"form",attrs:{"lazy-validation":""},on:{submit:function(e){return e.preventDefault(),t.submit(e)}},model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[n("v-row",[n("v-col",{attrs:{sm:"12"}},[n("v-text-field",{attrs:{label:"Insert your TFT Wallet Address",rules:t.addressRules,loading:t.loading},model:{value:t.address,callback:function(e){t.address=e},expression:"address"}}),n("v-btn",{staticClass:"primary",attrs:{type:"submit"},on:{click:t.validate}},[t._v(" create vesting account ")])],1)],1),n("v-row",[n("v-col",[n("span",[t._v("The vested tokens will be returned to your wallet according to these "),n("a",{attrs:{target:"blank",href:"https://new.threefold.io/info/threefold#/threefold__vesting_pool"}},[t._v("specifications")])])])],1)],1)},v=[],p={props:["getVestingInfo","setLoading"],name:"VestingForm",data:function(){return{loading:!1,valid:!0,address:null,addressRules:[function(t){return!!t||"Address is required"}]}},methods:{submit:function(){var t=this;this.setLoading(!0),u.createAccount(this.address).then((function(){t.$toasted.show("Created vesting account!",{type:"success",duration:5e3}),t.getVestingInfo()})).catch((function(e){t.setLoading(!1),console.log(e.response);var n=e.response.data;t.$toasted.show(n,{type:"error",duration:5e3})}))},validate:function(){this.$refs.form.validate()}}},g=p,h=(n("0673"),n("2877")),b=n("6544"),_=n.n(b),m=n("8336"),x=n("62ad"),w=n("4bd4"),V=n("0fd9"),y=n("8654"),C=Object(h["a"])(g,f,v,!1,null,"9eb73f02",null),A=C.exports;_()(C,{VBtn:m["a"],VCol:x["a"],VForm:w["a"],VRow:V["a"],VTextField:y["a"]});var k=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[t.loading?n("v-data-table",{staticClass:"elevation-1 mt-16",attrs:{"item-key":"name",loading:"","loading-text":"Loading... Please wait"}}):n("v-data-table",{staticClass:"elevation-1 mt-16",attrs:{headers:t.headers,items:t.vestinginfo,"items-per-page":5,"item-key":"owner","show-expand":"","single-expand":t.singleExpand,expanded:t.expanded},on:{"update:expanded":function(e){t.expanded=e}},scopedSlots:t._u([{key:"item.owner",fn:function(e){var a=e.item;return[n("div",[t._v(t._s(a.owner))])]}},{key:"item.vesting",fn:function(e){var a=e.item;return[n("div",[t._v(t._s(a.vesting))])]}},{key:"expanded-item",fn:function(t){var e=t.headers,a=t.item;return[n("td",{attrs:{colspan:e.length}},[n("AccountInfo",{key:a.id,attrs:{info:a}})],1)]}}])},[n("template",{slot:"no-data"},[t._v("No accounts added")])],2)],1)},T=[],O=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-col",[n("div",{staticClass:"title"},[t._v(" Account Information ")]),n("v-container",{attrs:{fluid:""}},[n("v-row",[n("v-flex",{staticClass:"text-left pr-2",attrs:{xs3:""}},[t._v("Owner Account Address ")]),n("v-flex",{staticClass:"text-truncate font-weight-bold"},[n("span",[t._v(t._s(t.info.owner))])])],1),n("v-row",[n("v-flex",{staticClass:"text-left pr-2",attrs:{xs3:""}},[t._v("Vesting Account Address ")]),n("v-flex",{staticClass:"text-truncate font-weight-bold"},[n("span",[t._v(t._s(t.info.vesting))])])],1),t._l(t.info.balances.vesting,(function(e){return n("v-row",{key:e.balance},[n("v-flex",{staticClass:"text-left pr-2 text-truncate",attrs:{xs3:""}},[t._v("Vested "+t._s(e.asset)+" ")]),n("v-flex",{staticClass:"text-truncate font-weight-bold"},[n("span",[t._v(t._s(e.balance))])])],1)})),n("v-row",[n("v-flex",{staticClass:"text-left pr-2",attrs:{xs3:""}},[t._v("Deposit TFT")])],1),n("v-row",[n("v-flex",{staticClass:"text-left pr-2",attrs:{xs3:""}},[n("VueQrcode",{attrs:{value:t.qrCodeValue}})],1)],1),n("v-row",[n("v-dialog",{attrs:{width:"700"},scopedSlots:t._u([{key:"activator",fn:function(e){var a=e.on,s=e.attrs;return[n("v-btn",t._g(t._b({attrs:{color:"blue lighten-2",dark:""}},"v-btn",s,!1),a),[t._v(" Check transactions ")])]}}]),model:{value:t.dialog,callback:function(e){t.dialog=e},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"headline"},[t._v("Transactions")]),n("v-card-subtitle",[t._v("for "+t._s(t.info.vesting))]),n("v-card-text",{staticClass:"pa-1"},[0===t.info.transactions.length?n("p",[t._v("No transactions yet!")]):n("ul",t._l(t.info.transactions,(function(e){return n("li",{key:e.transaction_hash},[t._v(" hash: "+t._s(e.transaction_hash)+" "),n("br"),t._v(" for "+t._s(e.amount)+" TFT "),n("br"),t._v(" at "+t._s(new Date(1e3*e.timestamp).toLocaleString("en-GB"))+" ")])})),0),t._t("default")],2),n("v-card-actions",[n("v-spacer"),t._t("actions")],2)],1)],1),n("v-btn",{staticClass:"ml-2",attrs:{color:"blue lighten-2",dark:"",href:t.stellarUrl+"/"+t.info.vesting,target:"_blank"}},[t._v(" Show Vesting account details ")])],1)],2)],1)},j=[],F=n("9a13"),I={props:["info"],components:{VueQrcode:F["a"]},data:function(){return{escrow:"",dialog:!1,dialogbalances:!1,stellarUrl:null}},mounted:function(){"STD"===this.info.network?this.stellarUrl="https://stellar.expert/explorer/public/account":this.stellarUrl="https://stellar.expert/explorer/testnet/account"},computed:{qrCodeValue:function(){return"TFT:".concat(this.info.vesting)}}},S=I,P=n("b0af"),L=n("99d9"),$=n("a523"),E=n("169a"),D=n("0e8f"),M=n("2fa4"),R=Object(h["a"])(S,O,j,!1,null,null,null),U=R.exports;_()(R,{VBtn:m["a"],VCard:P["a"],VCardActions:L["a"],VCardSubtitle:L["b"],VCardText:L["c"],VCardTitle:L["d"],VCol:x["a"],VContainer:$["a"],VDialog:E["a"],VFlex:D["a"],VRow:V["a"],VSpacer:M["a"]});var q={props:["vestinginfo","loading"],components:{AccountInfo:U},data:function(){return{headers:[{text:"Owner Account Address",value:"owner"},{text:"Vesting Account Address",value:"vesting"}],expanded:[],singleExpand:!0}},methods:{openAccountDetails:function(t){var e=this.expanded.indexOf(t);e>-1?this.expanded.splice(e,1):this.expanded.push(t)}}},B=q,z=n("8fea"),J=Object(h["a"])(B,k,T,!1,null,null,null),N=J.exports;_()(J,{VDataTable:z["a"]});var Q={name:"App",components:{VestingForm:A,AccountTable:N},mounted:function(){this.getVestingInfo()},data:function(){return{vestinginfo:[],loading:!1}},methods:{getVestingInfo:function(){var t=this;this.loading=!0,u.listAccounts().then((function(e){t.loading=!1,t.vestinginfo=e.data.data})).catch((function(e){t.loading=!1,console.log("Error! Could not reach the API. "+e)}))},setLoading:function(t){this.loading=t}}},G=Q,W=Object(h["a"])(G,r,i,!1,null,null,null),H=W.exports,K={name:"App",components:{Overview:H}},X=K,Y=(n("faee"),n("7496")),Z=n("adda"),tt=n("f6c4"),et=Object(h["a"])(X,s,o,!1,null,"660a0752",null),nt=et.exports;_()(et,{VApp:Y["a"],VContainer:$["a"],VImg:Z["a"],VMain:tt["a"]});var at=n("f309");a["a"].use(at["a"]);var st=new at["a"]({}),ot=n("a65d"),rt=n.n(ot);a["a"].config.productionTip=!1,a["a"].use(rt.a),new a["a"]({vuetify:st,render:function(t){return t(nt)}}).$mount("#app")},6018:function(t,e,n){},da3f:function(t,e,n){t.exports=n.p+"img/3fold_logo.d9027e1c.png"},faee:function(t,e,n){"use strict";n("20f8")}});
//# sourceMappingURL=app.dd5dd591.js.map