import * as THREE from 'three';

// Standalone, original low-poly environment prefabs. Import and place these
// explicitly from a stage builder; this module never edits a world or track.
const standard=(color:number,roughness=1)=>new THREE.MeshStandardMaterial({color,roughness,flatShading:true});
const fur=standard(0x716252),furLight=standard(0xa49378),mask=standard(0x272629),belly=standard(0xd5c8ae),eye=standard(0xffe5a1,.5),black=standard(0x17191c),red=standard(0xb94737),cream=standard(0xe6d7b7);
function ico(parent:THREE.Group,name:string,material:THREE.Material,pos:THREE.Vector3,scale:THREE.Vector3,detail=1){
  const mesh=new THREE.Mesh(new THREE.IcosahedronGeometry(1,detail),material);mesh.name=name;mesh.position.copy(pos);mesh.scale.copy(scale);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
}
function rod(parent:THREE.Group,name:string,a:THREE.Vector3,b:THREE.Vector3,r:number,material:THREE.Material,radial=5){
  const delta=b.clone().sub(a),mesh=new THREE.Mesh(new THREE.CylinderGeometry(r*.82,r,delta.length(),radial,1),material);mesh.name=name;mesh.position.copy(a).add(b).multiplyScalar(.5);mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize());mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
}

/** Original compact raccoon pit-crew mascot; inspired by the round viral raccoon silhouette, not a copied photo. */
export function createJimmothyMascot(){
  const root=new THREE.Group();root.name='crazykids-jimmothy-mascot';
  ico(root,'round-body',fur,new THREE.Vector3(0,.52,0),new THREE.Vector3(.45,.47,.39),2);
  ico(root,'cream-bib',belly,new THREE.Vector3(0,.43,.305),new THREE.Vector3(.27,.29,.10),1);
  ico(root,'round-head',furLight,new THREE.Vector3(0,1.06,.04),new THREE.Vector3(.34,.32,.31),2);
  for(const side of [-1,1]){
    ico(root,'dark-ear-'+side,mask,new THREE.Vector3(side*.235,1.29,.035),new THREE.Vector3(.115,.13,.09),1);
    ico(root,'ear-inner-'+side,furLight,new THREE.Vector3(side*.235,1.295,.105),new THREE.Vector3(.055,.068,.025),1);
    ico(root,'eye-mask-'+side,mask,new THREE.Vector3(side*.135,1.09,.292),new THREE.Vector3(.15,.105,.055),1);
    ico(root,'eye-'+side,eye,new THREE.Vector3(side*.13,1.105,.343),new THREE.Vector3(.038,.038,.018),1);
    ico(root,'boot-'+side,black,new THREE.Vector3(side*.235,.12,.12),new THREE.Vector3(.17,.12,.22),1);
  }
  ico(root,'muzzle',belly,new THREE.Vector3(0,.965,.32),new THREE.Vector3(.18,.12,.09),1);
  ico(root,'nose',black,new THREE.Vector3(0,1.005,.405),new THREE.Vector3(.052,.04,.028),1);
  // A short raised tail uses broad alternating bands, readable at rally scale.
  const tail=[new THREE.Vector3(.27,.40,-.27),new THREE.Vector3(.48,.28,-.48),new THREE.Vector3(.66,.36,-.60),new THREE.Vector3(.77,.55,-.62)];
  for(let i=0;i<tail.length-1;i++)rod(root,'ring-tail-band-'+i,tail[i],tail[i+1],.105,i%2?mask:furLight,5);
  // Tiny red crew scarf gives this mascot a CrazyKids accent.
  const scarf=ico(root,'crew-scarf',red,new THREE.Vector3(0,.79,.31),new THREE.Vector3(.27,.075,.09),1);scarf.rotation.z=-.08;
  root.userData.assetInfo={category:'environment-prop',placement:'not placed',style:'faceted low-poly'};
  return root;
}

/** Small 3D joke board with an independently usable sign face. */
export function createSnackMarshalSign(){
  const root=new THREE.Group();root.name='crazykids-snack-marshal-sign';
  const board=new THREE.Mesh(new THREE.BoxGeometry(1.18,.70,.10),red);board.name='red-sign-board';board.position.y=1.22;board.castShadow=true;root.add(board);
  const postMat=standard(0x514538);rod(root,'left-post',new THREE.Vector3(-.39,0,0),new THREE.Vector3(-.39,.91,0),.045,postMat,5);rod(root,'right-post',new THREE.Vector3(.39,0,0),new THREE.Vector3(.39,.91,0),.045,postMat,5);
  const signMaterial=new THREE.MeshBasicMaterial({color:0xe6d7b7,side:THREE.DoubleSide});
  const face=new THREE.Mesh(new THREE.PlaneGeometry(1.04,.56),signMaterial);face.name='sign-art-face';face.position.set(0,1.22,.057);root.add(face);
  const textureCanvas=document.createElement('canvas');textureCanvas.width=512;textureCanvas.height=256;
  const ctx=textureCanvas.getContext('2d');if(ctx){ctx.fillStyle='#e6d7b7';ctx.fillRect(0,0,512,256);ctx.fillStyle='#292721';ctx.textAlign='center';ctx.font='900 48px sans-serif';ctx.fillText('JIMMOTHY SAYS',256,95);ctx.fillStyle='#b94737';ctx.font='900 60px sans-serif';ctx.fillText('PIT FOR SNACKS',256,175)}
  const tex=new THREE.CanvasTexture(textureCanvas);tex.colorSpace=THREE.SRGBColorSpace;signMaterial.map=tex;signMaterial.needsUpdate=true;
  root.userData.assetInfo={category:'environment-prop',placement:'not placed',text:'JIMMOTHY SAYS: PIT FOR SNACKS'};
  return root;
}

/** Four-color leaf scatter mesh for a road-edge patch or ground-detail system. */
export function createAutumnLeafScatter(seed=17,count=18){
  const root=new THREE.Group();root.name='crazykids-autumn-leaf-scatter';
  const colors=[0xc95735,0xd8913e,0x94713b,0x6e823d].map(c=>standard(c));
  let x=seed>>>0;const rand=()=>((x=(Math.imul(1664525,x)+1013904223)>>>0)/4294967296);
  for(let i=0;i<count;i++){
    const leaf=ico(root,'polygon-leaf-'+i,colors[i%colors.length],new THREE.Vector3((rand()-.5)*1.6,.018+i*.0005,(rand()-.5)*1.6),new THREE.Vector3(.12+rand()*.11,.018,.055+rand()*.07),0);
    leaf.rotation.y=rand()*Math.PI*2;leaf.rotation.z=(rand()-.5)*.16;
  }
  root.userData.assetInfo={category:'ground-detail',placement:'not placed',seed,count};return root;
}
