(function(){"use strict";var e={3619:function(e,n,o){var t=o(5130),i=o(6768);const r={id:"app"},a={class:"content"};function s(e,n,o,t,s,c){const l=(0,i.g2)("HamburgerMenu"),u=(0,i.g2)("router-view"),v=(0,i.g2)("NavBar");return(0,i.uX)(),(0,i.CE)("div",r,[(0,i.bF)(l),(0,i.Lk)("div",a,[(0,i.bF)(u)]),(0,i.bF)(v)])}var c=o(4232);const l={class:"menu-content"};function u(e,n,o,r,a,s){return(0,i.uX)(),(0,i.CE)(i.FK,null,[(0,i.Lk)("div",{class:"hamburger-menu",onClick:n[0]||(n[0]=(...e)=>s.toggleMenu&&s.toggleMenu(...e))},[(0,i.Lk)("div",{class:(0,c.C4)(["bar",{active:a.isOpen}])},null,2),(0,i.Lk)("div",{class:(0,c.C4)(["bar",{active:a.isOpen}])},null,2),(0,i.Lk)("div",{class:(0,c.C4)(["bar",{active:a.isOpen}])},null,2)]),(0,i.bF)(t.eB,{name:"menu-slide",onBeforeEnter:s.beforeEnter,onEnter:s.enter,onLeave:s.leave},{default:(0,i.k6)((()=>[(0,i.bo)((0,i.Lk)("div",l,n[1]||(n[1]=[(0,i.Lk)("h4",null,"This is the menu content! Add your links or navigation here.",-1)]),512),[[t.aG,a.isOpen]])])),_:1},8,["onBeforeEnter","onEnter","onLeave"])],64)}var v={name:"HamburgerMenu",data(){return{isOpen:!1}},methods:{toggleMenu(){this.isOpen=!this.isOpen},beforeEnter(e){e.style.transform="translateX(100%)",e.style.opacity="0"},enter(e,n){e.offsetHeight,e.style.transition="transform 0.3s ease-in-out, opacity 0.3s ease-in-out",e.style.transform="translateX(0)",e.style.opacity="1",n()},leave(e,n){e.style.opacity="0",n()}}},g=o(1241);const d=(0,g.A)(v,[["render",u],["__scopeId","data-v-4f0e4d80"]]);var f=d;o(4114);const m={class:"pos-nav"},p=["src"],h=["src"],b=["src"];function w(e,n,o,t,r,a){return(0,i.uX)(),(0,i.CE)("div",m,[(0,i.Lk)("div",{onClick:n[0]||(n[0]=n=>e.$router.push("/compare-shoes")),class:"pos-icon"},[(0,i.Lk)("img",{src:t.imageSource1},null,8,p)]),(0,i.Lk)("div",{onClick:n[1]||(n[1]=n=>e.$router.push("/")),class:"pos-icon"},[(0,i.Lk)("img",{src:t.imageSource2},null,8,h)]),(0,i.Lk)("div",{onClick:n[2]||(n[2]=n=>e.$router.push("/shoe-finder")),class:"pos-icon"},[(0,i.Lk)("img",{src:t.imageSource3},null,8,b)])])}var k=o(1387),y={name:"NavBar",setup(){const e=(0,k.lq)(),n=(0,i.EW)((()=>e.path.includes("compare"))),t=(0,i.EW)((()=>"/"===e.path)),r=(0,i.EW)((()=>e.path.includes("finder"))),a=(0,i.EW)((()=>n.value?o(1904):o(8205))),s=(0,i.EW)((()=>t.value?o(470):o(7905))),c=(0,i.EW)((()=>r.value?o(5769):o(3386)));return{imageSource1:a,imageSource2:s,imageSource3:c,isCompareRoute:n,isHomeRoute:t,isShoeFinderRoute:r}}};const C=(0,g.A)(y,[["render",w]]);var L=C,P=(0,i.pM)({name:"App",components:{HamburgerMenu:f,NavBar:L}});const x=(0,g.A)(P,[["render",s]]);var E=x,S=o.p+"img/profile-circle.31e7afc4.svg";const O={key:0,class:"width"},N={class:"main"},M={class:"container top"},_={class:"content top-c"},T={style:{display:"flex","flex-direction":"row"}},A={class:"container"},D={class:"content progress-bar"},I={style:{display:"flex","flex-direction":"column"}},R={class:"container"},F={class:"content km-ran"},X={class:"center"},H={class:"container"},z={class:"center"},B={class:"margin name"},V={class:"margin shoe"},W={key:1};function j(e,n,o,t,r,a){const s=(0,i.g2)("ShoeViewer");return t.profileClicked?((0,i.uX)(),(0,i.CE)("div",W,[n[5]||(n[5]=(0,i.Lk)("p",null,"Profile page",-1)),(0,i.Lk)("button",{onClick:n[1]||(n[1]=(...e)=>t.profilePage&&t.profilePage(...e))},"Go back")])):((0,i.uX)(),(0,i.CE)("div",O,[n[4]||(n[4]=(0,i.Lk)("h1",{class:"title"},"CUSHIONING STATE",-1)),(0,i.Lk)("div",N,[(0,i.Lk)("div",M,[(0,i.Lk)("div",_,[(0,i.bF)(s)])]),(0,i.Lk)("div",T,[(0,i.Lk)("div",A,[(0,i.Lk)("div",D,[(0,i.Lk)("div",{class:"progress",style:(0,c.Tr)({height:t.cushioningPercentage+"%"})},null,4)])]),(0,i.Lk)("div",I,[(0,i.Lk)("div",R,[(0,i.Lk)("div",F,[(0,i.Lk)("div",X,[(0,i.Lk)("h1",null,(0,c.v_)(t.kmRan)+" KM",1),n[2]||(n[2]=(0,i.Lk)("h4",null,"RAN",-1))])])]),(0,i.Lk)("div",H,[(0,i.Lk)("div",{onClick:n[0]||(n[0]=(...e)=>t.profilePage&&t.profilePage(...e)),class:"content profile"},[(0,i.Lk)("div",z,[n[3]||(n[3]=(0,i.Lk)("img",{class:"profile-img",src:S},null,-1)),(0,i.Lk)("h3",B,(0,c.v_)(t.name),1),(0,i.Lk)("h4",V,(0,c.v_)(t.shoe),1)])])])])])])]))}var K=o(144);const Z={id:"shoe-viewer"},q={ref:"canvas"};function G(e,n,o,t,r,a){return(0,i.uX)(),(0,i.CE)("div",Z,[n[0]||(n[0]=(0,i.Lk)("div",{class:"bg"},null,-1)),(0,i.Lk)("canvas",q,null,512)])}o(8992),o(3949);var $=o(8776),J=o(1353),Y=o(2951);let Q,U,ee,ne,oe,te,ie=0;const re=[{r:20,g:224,b:97},{r:128,g:255,b:0},{r:255,g:255,b:0},{r:255,g:200,b:0},{r:255,g:165,b:0},{r:255,g:100,b:0},{r:255,g:0,b:0},{r:200,g:0,b:0},{r:255,g:0,b:125}],ae=[{r:20,g:224,b:97},{r:245,g:245,b:255},{r:255,g:255,b:0},{r:255,g:200,b:0},{r:255,g:165,b:0},{r:255,g:100,b:0},{r:255,g:0,b:0},{r:200,g:0,b:0},{r:255,g:0,b:125},{r:255,g:0,b:255}];function se(e){const n=document.getElementById("shoe-viewer");ee=new $.JeP({canvas:e,antialias:!0}),ee.setSize(n.clientWidth,n.clientHeight),ee.setClearColor(0,0),ee.setPixelRatio(window.devicePixelRatio),ee.shadowMap.enabled=!0,ee.shadowMap.type=$.Wk7,Q=new $.Z58;const o=n.clientWidth/n.clientHeight;U=new $.ubm(25,o,1,1e3),U.position.set(4,5,12),ne=new Y.N(U,ee.domElement),ne.enableDamping=!0,ne.enablePan=!1,ne.minDistance=8,ne.maxDistance=12,ne.minPolarAngle=.6,ne.maxPolarAngle=.6*Math.PI,ne.target.set(0,0,0),ne.update();const t=[new $.ZyN(16777215,20),new $.ZyN(16777215,20),new $.ZyN(16777215,10),new $.ZyN(16777215,10),new $.$p8(16777215,10)];t[0].position.set(0,10,0),t[1].position.set(0,-10,0),t[2].position.set(-10,0,0),t[3].position.set(10,0,0),t[4].position.set(0,0,0),t.forEach((e=>Q.add(e)));const i=new $.YJl;Q.add(i);const r=new J.B;r.load("Shoes-Make.gltf",(e=>{oe=e.scene;const n=(new $.NRn).setFromObject(oe),o=n.getCenter(new $.Pq0);oe.position.sub(o),le(),i.add(oe)})),te=ce();const a=new $.zD7;function s(){const e=a.getElapsedTime();te&&(te.uniforms.time.value=e),ee.render(Q,U),ne.update(),requestAnimationFrame(s)}s()}function ce(){return new $.BKk({uniforms:{time:{value:0},lightDirection:{value:new $.Pq0(1,1,1).normalize()},rw:{value:ae[ie+1].r/255},gw:{value:ae[ie+1].g/255},bw:{value:ae[ie+1].b/255},r:{value:re[ie].r/255},g:{value:re[ie].g/255},b:{value:re[ie].b/255}},vertexShader:"\n            varying vec3 vNormal;\n            varying vec3 vViewPosition;\n            \n            void main() {\n                // Compute normal and view position in the vertex shader for later use\n                vNormal = normalize(normalMatrix * normal);\n                vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);\n                vViewPosition = -viewPosition.xyz;\n\n                // Final position of vertex\n                gl_Position = projectionMatrix * viewPosition;\n            }\n        ",fragmentShader:"\n            uniform float time;\n            uniform vec3 lightDirection;\n            uniform float rw, gw, bw, r, g, b;\n            \n            varying vec3 vNormal;\n            varying vec3 vViewPosition;\n\n            // Function for color cycling between two colors over time\n            vec3 getColorCycle(float t) {\n                vec3 bright = vec3(r, g, b);\n                vec3 white = vec3(rw, gw, bw);\n                \n                // Normalize time for a consistent cycle duration\n                t = mod(t, 1.25); \n                \n                // Smooth transitions using easing functions\n                float easedT = smoothstep(0.0, 0.25, t); \n                float easedReverseT = pow(smoothstep(0.5, 1.0, t), 3.0);\n\n                // Transition to white and back to bright\n                if (t < 0.5) {\n                    return mix(bright, white, easedT); \n                } else {\n                    return mix(white, bright, easedReverseT); \n                }\n            }\n\n            void main() {\n                // Set cycle time for slower color cycling\n                float cycleTime = mod(time * 0.6, 1.25);\n                vec3 colorCycle = getColorCycle(cycleTime);\n                \n                // Lighting calculations\n                vec3 normal = normalize(vNormal);\n                vec3 lightDir = normalize(lightDirection);\n                vec3 viewDir = normalize(vViewPosition);\n\n                // Diffuse component based on the angle to the light source\n                float diff = max(dot(normal, lightDir), 0.0);\n\n                // Specular reflection for added shininess\n                vec3 reflectDir = reflect(-lightDir, normal);\n                float spec = pow(max(dot(viewDir, reflectDir), 0.0), 12.0) * 0.8;\n\n                // Combine diffuse and specular lighting with color cycle\n                vec3 finalColor = (colorCycle * (diff * 0.8)) + vec3(1.0) * spec * 0.5;\n\n                // Output the final fragment color\n                gl_FragColor = vec4(finalColor, 1.0);\n            }\n        "})}function le(){oe.traverse((e=>{e.isMesh&&(e.castShadow=!0,e.receiveShadow=!0,e.material="Plane"===e.name||"Plane_1"===e.name?te:new $.tXL({color:new $.Q1f(0,0,0),shininess:10}))}))}function ue(e){console.log("Incoming value:",e,"Type:",typeof e);const n=Number(e);isNaN(n)?console.warn("Provided value is not a number:",e):(ie=Math.max(0,Math.min(re.length-1,n)),te&&(ie+1<ae.length?(te.uniforms.rw.value=ae[ie+1].r/255,te.uniforms.gw.value=ae[ie+1].g/255,te.uniforms.bw.value=ae[ie+1].b/255):console.warn("cushioningStateShoeColor index out of bounds for stateIndex + 1:",ie+1),te.uniforms.r.value=ae[ie].r/255,te.uniforms.g.value=ae[ie].g/255,te.uniforms.b.value=ae[ie].b/255),le())}var ve={name:"ShoeViewer",setup(){const e=(0,K.KR)(null),n=(0,K.KR)(0);(0,i.sV)((()=>{se(e.value)}));const o=()=>{ue(n.value)};return{canvas:e,colorIndex:n,updateColor:o}}};const ge=(0,g.A)(ve,[["render",G],["__scopeId","data-v-157ea5ee"]]);var de=ge,fe={name:"CushioningStatePage",components:{ShoeViewer:de},setup(){let e=12,n="TIMOTHY",o="Assics GEL-EXCITE 10",t=(0,K.KR)(!1),i=80;const r=()=>{t.value=!t.value,console.log(t.value)};return{kmRan:e,profilePage:r,name:n,shoe:o,profileClicked:t,cushioningPercentage:i}}};const me=(0,g.A)(fe,[["render",j],["__scopeId","data-v-60a4d5f7"]]);var pe=me;const he={class:"width"};function be(e,n,o,t,r,a){return(0,i.uX)(),(0,i.CE)("div",he,n[0]||(n[0]=[(0,i.Lk)("h1",{class:"title"},"SHOE COMPARISON",-1)]))}var we={name:"ComparePage"};const ke=(0,g.A)(we,[["render",be],["__scopeId","data-v-581aef2a"]]);var ye=ke;const Ce={class:"width"};function Le(e,n,o,t,r,a){return(0,i.uX)(),(0,i.CE)("div",Ce,n[0]||(n[0]=[(0,i.Lk)("h1",{class:"title"},"SHOE FINDER",-1)]))}var Pe={name:"ComparePage"};const xe=(0,g.A)(Pe,[["render",Le],["__scopeId","data-v-728b5e46"]]);var Ee=xe;const Se=[{path:"/",name:"CushioningStatePage",component:pe},{path:"/compare-shoes",name:"ComparePage",component:ye},{path:"/shoe-finder",name:"ShoeFinderPage",component:Ee}],Oe=(0,k.aE)({history:(0,k.LA)(),routes:Se});var Ne=Oe;(0,t.Ef)(E).use(Ne).mount("#app")},1904:function(e,n,o){e.exports=o.p+"img/Compare-active.20ac055c.svg"},8205:function(e,n,o){e.exports=o.p+"img/Compare.878934d5.svg"},470:function(e,n,o){e.exports=o.p+"img/Cushioning-state-active.59eb8596.svg"},5769:function(e,n,o){e.exports=o.p+"img/Shoe-finder-active.a9b9c0af.svg"},3386:function(e,n,o){e.exports=o.p+"img/Shoe-finder.40775fdd.svg"},7905:function(e,n,o){e.exports=o.p+"img/Shoe.d9ab8587.svg"}},n={};function o(t){var i=n[t];if(void 0!==i)return i.exports;var r=n[t]={exports:{}};return e[t].call(r.exports,r,r.exports,o),r.exports}o.m=e,function(){var e=[];o.O=function(n,t,i,r){if(!t){var a=1/0;for(u=0;u<e.length;u++){t=e[u][0],i=e[u][1],r=e[u][2];for(var s=!0,c=0;c<t.length;c++)(!1&r||a>=r)&&Object.keys(o.O).every((function(e){return o.O[e](t[c])}))?t.splice(c--,1):(s=!1,r<a&&(a=r));if(s){e.splice(u--,1);var l=i();void 0!==l&&(n=l)}}return n}r=r||0;for(var u=e.length;u>0&&e[u-1][2]>r;u--)e[u]=e[u-1];e[u]=[t,i,r]}}(),function(){o.n=function(e){var n=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(n,{a:n}),n}}(),function(){o.d=function(e,n){for(var t in n)o.o(n,t)&&!o.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:n[t]})}}(),function(){o.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){o.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)}}(),function(){o.p="/"}(),function(){var e={524:0};o.O.j=function(n){return 0===e[n]};var n=function(n,t){var i,r,a=t[0],s=t[1],c=t[2],l=0;if(a.some((function(n){return 0!==e[n]}))){for(i in s)o.o(s,i)&&(o.m[i]=s[i]);if(c)var u=c(o)}for(n&&n(t);l<a.length;l++)r=a[l],o.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return o.O(u)},t=self["webpackChunkhci_proto"]=self["webpackChunkhci_proto"]||[];t.forEach(n.bind(null,0)),t.push=n.bind(null,t.push.bind(t))}();var t=o.O(void 0,[504],(function(){return o(3619)}));t=o.O(t)})();
//# sourceMappingURL=app.8e9fa7e0.js.map