(function(e){function t(t){for(var r,A,c=t[0],s=t[1],i=t[2],d=0,l=[];d<c.length;d++)A=c[d],Object.prototype.hasOwnProperty.call(a,A)&&a[A]&&l.push(a[A][0]),a[A]=0;for(r in s)Object.prototype.hasOwnProperty.call(s,r)&&(e[r]=s[r]);u&&u(t);while(l.length)l.shift()();return o.push.apply(o,i||[]),n()}function n(){for(var e,t=0;t<o.length;t++){for(var n=o[t],r=!0,c=1;c<n.length;c++){var s=n[c];0!==a[s]&&(r=!1)}r&&(o.splice(t--,1),e=A(A.s=n[0]))}return e}var r={},a={app:0},o=[];function A(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,A),n.l=!0,n.exports}A.m=e,A.c=r,A.d=function(e,t,n){A.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},A.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},A.t=function(e,t){if(1&t&&(e=A(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(A.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)A.d(n,r,function(t){return e[t]}.bind(null,r));return n},A.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return A.d(t,"a",t),t},A.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},A.p="/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],s=c.push.bind(c);c.push=t,c=c.slice();for(var i=0;i<c.length;i++)t(c[i]);var u=s;o.push([1,"chunk-vendors"]),n()})({0:function(e,t){},1:function(e,t,n){e.exports=n("56d7")},2:function(e,t){},3:function(e,t){},"32a8":function(e,t,n){"use strict";var r=n("c755"),a=n.n(r);a.a},4:function(e,t){},5:function(e,t){},"56d7":function(e,t,n){"use strict";n.r(t);n("e623"),n("e379"),n("5dc8"),n("37e1");var r=n("2b0e"),a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-app",[r("v-img",{staticClass:"logo",attrs:{src:n("d07c")}}),r("v-content",{attrs:{"fill-height":""}},[r("v-layout",{attrs:{"justify-center":"","fill-height":""}},[r("v-layout",{attrs:{column:"","align-center":"","justify-center":""}},[r("router-view")],1)],1)],1)],1)},o=[],A={name:"App"},c=A,s=(n("cdb6"),n("2877")),i=n("6544"),u=n.n(i),d=n("7496"),l=n("a75b"),p=n("adda"),f=n("a722"),b=Object(s["a"])(c,a,o,!1,null,"2e4e42d6",null),v=b.exports;u()(b,{VApp:d["a"],VContent:l["a"],VImg:p["a"],VLayout:f["a"]});var g=n("f309");r["a"].use(g["a"]);var h,y,m=new g["a"]({theme:{dark:!1,themes:{dark:{primary:"#57be8e"},light:{primary:"#57be8e"}}}}),w=n("a65d"),B=n.n(w),O=n("8c4f"),x=(n("99af"),n("96cf"),n("1da1")),j={botFrontEnd:"https://login.threefold.me",botBackend:"https://login.threefold.me/",redirect_url:"".concat("/","/#/callback"),appId:window.location.host,seedPhrase:"weather smooth little world side palace green armor busy view solution escape"},_=(n("d3b7"),n("427a")),P=n("7dee"),k=n("29c9"),R={validateSignature:function(e,t,n){return new Promise(function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(r){var a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,P.ready;case 2:n=Object(_["decodeBase64"])(n),t=Object(_["decodeBase64"])(t),a=P.crypto_sign_open(t,n),r(a);case 6:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}())},decrypt:function(e,t,n,r){return new Promise(function(){var a=Object(x["a"])(regeneratorRuntime.mark((function a(o){var A;return regeneratorRuntime.wrap((function(a){while(1)switch(a.prev=a.next){case 0:return e=Object(_["decodeBase64"])(e),a.next=3,P.ready;case 3:n=P.crypto_sign_ed25519_sk_to_curve25519(Object(_["decodeBase64"])(n)),r=P.crypto_sign_ed25519_pk_to_curve25519(Object(_["decodeBase64"])(r)),t=Object(_["decodeBase64"])(t),A=P.crypto_box_open_easy(e,t,r,n),A=Object(_["encodeUTF8"])(A),o(A);case 9:case"end":return a.stop()}}),a)})));return function(e){return a.apply(this,arguments)}}())},validateSignedAttempt:function(e,t){return new Promise(function(){var n=Object(x["a"])(regeneratorRuntime.mark((function n(r,a){var o;return regeneratorRuntime.wrap((function(n){while(1)switch(n.prev=n.next){case 0:return n.next=2,P.ready;case 2:t=Object(_["decodeBase64"])(t),e=Object(_["decodeBase64"])(e),o=P.crypto_sign_open(e,t),o||a("Invalid signature."),r(o);case 7:case"end":return n.stop()}}),n)})));return function(e,t){return n.apply(this,arguments)}}())},encrypt:function(e,t,n){return new Promise(function(){var r=Object(x["a"])(regeneratorRuntime.mark((function r(a){var o,A;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e=(new TextEncoder).encode(e),r.next=3,P.ready;case 3:t=P.crypto_sign_ed25519_sk_to_curve25519(Object(_["decodeBase64"])(t)),n=P.crypto_sign_ed25519_pk_to_curve25519(Object(_["decodeBase64"])(n)),o=P.randombytes_buf(P.crypto_secretbox_NONCEBYTES),A=P.crypto_box_easy(e,o,n,t),a({encrypted:Object(_["encodeBase64"])(A),nonce:Object(_["encodeBase64"])(o)});case 8:case"end":return r.stop()}}),r)})));return function(e){return r.apply(this,arguments)}}())},generateKeys:function(e){return new Promise(function(){var t=Object(x["a"])(regeneratorRuntime.mark((function t(n){var r,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,P.ready;case 2:e||(e=k.entropyToMnemonic(P.randombytes_buf(P.crypto_box_SEEDBYTES/2))),r=(new TextEncoder).encode(k.mnemonicToEntropy(e)),a=P.crypto_sign_seed_keypair(r),n({phrase:e,privateKey:Object(_["encodeBase64"])(a.privateKey),publicKey:Object(_["encodeBase64"])(a.publicKey)});case 6:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}())},getEdPkInCurve:function(e){return Object(_["encodeBase64"])(P.crypto_sign_ed25519_pk_to_curve25519(Object(_["decodeBase64"])(e)))}},E=n("4487"),F={name:"login",data:function(){return{privateKey:null,publicKey:null,privateKey2:null,publicKey2:null,message:null,encrypted:null,decrypted:null,nonce:null}},mounted:function(){this.login()},methods:{login:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(){var t,n,r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t=E.generate(),window.localStorage.setItem("state",t),e.next=4,R.generateKeys(j.seedPhrase);case 4:n=e.sent,r=j.appId,window.location.href="".concat(j.botFrontEnd,"?state=").concat(t,"&appid=").concat(r,"&publickey=").concat(encodeURIComponent(R.getEdPkInCurve(n.publicKey)),"&redirecturl=").concat(encodeURIComponent(j.redirect_url));case 7:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}(),redirect:function(){var e=Object(x["a"])(regeneratorRuntime.mark((function e(t,n,r,a,o){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:window.location.href="".concat(j.botFrontEnd,"?state=").concat(t,"&scope=").concat(n,"&appid=").concat(r,"&publickey=").concat(encodeURIComponent(R.getEdPkInCurve(a)),"&redirecturl=").concat(encodeURIComponent(o));case 1:case"end":return e.stop()}}),e)})));function t(t,n,r,a,o){return e.apply(this,arguments)}return t}()}},S=F,C=Object(s["a"])(S,h,y,!1,null,null,null),V=C.exports,I=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-app",{attrs:{id:"inspire"}},[r("v-container",{staticClass:"fill-height",attrs:{fluid:""}},[r("v-row",{attrs:{align:"center",justify:"center"}},[r("v-col",{attrs:{cols:"3",sm:"4",md:"6",lg:"12"}},[r("v-img",{staticClass:"logo",attrs:{src:n("6ff6")}}),r("div",{staticClass:"header"},[r("h1",[e._v("Get FreeTFT's")])]),r("div",{staticClass:"content"},[r("div",{},[r("v-text-field",{attrs:{label:"Enter Stellar address here",rules:e.rules,"hide-details":"auto"},model:{value:e.address,callback:function(t){e.address=t},expression:"address"}}),e.error?r("p",{attrs:{id:"errortext"}},[e._v("This address probably does not exist or does not have a trustline with the issuer of our Stellar FreeTFT. Or this address might already have requested tokens before!")]):e._e()],1),r("br"),r("br"),r("p",[e._v("Enter a valid Stellar address to receive FreeTFT, this address must have a trustline to the FreeTFT issuer! You will only be able to receive tokens once.")]),r("br"),r("br"),r("v-btn",{staticClass:"ma-2",attrs:{outlined:"",color:"#333333",loading:e.loading,disabled:e.loading||""===e.address},on:{click:function(t){return e.fundAddress()}}},[e._v(" Receive your FreeTFT ")])],1)],1)],1)],1)],1)},L=[],Q=n("bc3a"),W=n.n(Q);function z(e,t){return W.a.post("/threefoldfoundation/stellar_faucet/actors/stellar_faucet/transfer",{args:{destination:e,signed_attempt_object:t}})}var K={data(){return{error:!1,address:"",loading:!1,signedAttemptObject:void 0,username:void 0}},async mounted(){let e=new URL(window.location.href),t=e.searchParams.get("error");t&&console.log("Error: ",t)},methods:{fundAddress(){this.loading=!0,this.error=!1;let e=new URL(window.location.href);const t=e.hash.split("?")[1];let n=new URLSearchParams(t);const r=n.get("signedAttempt"),a=JSON.parse(r);z(this.address,a).then(e=>{200==e.status?(this.loading=!1,this.$toasted.success("Address funded successfully")):this.error=!0}).catch(e=>{console.log(e.meta),this.error=!0,this.loading=!1})}},name:"FundAccount"},U=K,T=(n("32a8"),n("8336")),q=n("62ad"),H=n("a523"),M=n("0fd9b"),X=n("8654"),Z=Object(s["a"])(U,I,L,!1,null,"49b2b018",null),D=Z.exports;u()(Z,{VApp:d["a"],VBtn:T["a"],VCol:q["a"],VContainer:H["a"],VImg:p["a"],VRow:M["a"],VTextField:X["a"]}),r["a"].use(O["a"]);var Y=new O["a"]({base:"/",routes:[{path:"/",name:"login",component:V},{path:"/callback",name:"callback",component:D}]});r["a"].config.productionTip=!1,r["a"].use(B.a,{duration:3e3,theme:"bubble",position:"bottom-center"}),new r["a"]({vuetify:m,router:Y,render:function(e){return e(v)}}).$mount("#app")},"6ff6":function(e,t,n){e.exports=n.p+"img/faucet-logo.75f793cc.png"},c755:function(e,t,n){},cdb6:function(e,t,n){"use strict";var r=n("e8b1"),a=n.n(r);a.a},d07c:function(e,t){e.exports="data:image/png;base64,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"},e8b1:function(e,t,n){}});
//# sourceMappingURL=app.c08d8bcd.js.map