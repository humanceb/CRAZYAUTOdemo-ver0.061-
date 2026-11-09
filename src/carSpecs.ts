import evoX from './carSpecs/evo_x.json';
import sti from './carSpecs/sti_gd.json';
import evo3 from './carSpecs/evo_iii.json';
import quattro from './carSpecs/quattro_s1.json';
import rs6 from './carSpecs/rs6_c8.json';

// Source: CrazyAuto-Demo/assets/cars, the earlier CrazyKids physics build.
// New cars use the same four-wheel solver; these are gameplay estimates, not
// factory-measured tire, suspension, or drivetrain calibrations.
const grYaris={...evoX,name:'GR Yaris - stylized recreation',model_id:'gr_yaris',mass_kg:1280,wheelbase_m:2.56,track_width_m:1.54,front_weight_fraction:.57,yaw_inertia_kgm2:1850,max_drive_torque_nm:2600,max_brake_torque_nm:2500,front_drive_fraction:.50};
const delta={...evo3,name:'Delta HF Integrale - stylized recreation',model_id:'delta_integrale',mass_kg:1350,wheelbase_m:2.48,track_width_m:1.50,front_weight_fraction:.58,yaw_inertia_kgm2:1900,max_drive_torque_nm:2700};
const p205={...quattro,name:'205 Turbo 16 - stylized recreation',model_id:'205_t16',mass_kg:1130,wheelbase_m:2.54,track_width_m:1.47,front_weight_fraction:.45,yaw_inertia_kgm2:1750,max_drive_torque_nm:2750,front_drive_fraction:.42};
const celica={...sti,name:'Celica GT-Four ST205 - stylized recreation',model_id:'celica_st205',mass_kg:1390,wheelbase_m:2.535,track_width_m:1.51,front_weight_fraction:.59,yaw_inertia_kgm2:2120,max_drive_torque_nm:2800,front_drive_fraction:.50};
const rs200={...quattro,name:'RS200 - stylized recreation',model_id:'rs200',mass_kg:1160,wheelbase_m:2.53,track_width_m:1.53,front_weight_fraction:.46,yaw_inertia_kgm2:1800,max_drive_torque_nm:2900,front_drive_fraction:.46};
const trail={...rs6,name:'CK Trail 4x4 - original CrazyKids concept',model_id:'ck_trail',mass_kg:2250,wheelbase_m:2.70,track_width_m:1.78,cg_height_m:.74,front_weight_fraction:.55,yaw_inertia_kgm2:4300,roll_inertia_kgm2:2200,wheel_radius_m:.39,max_drive_torque_nm:3900,front_drive_fraction:.48};
export const carSpecs={evoX,sti,evo3,quattro,rs6,grYaris,delta,p205,celica,rs200,trail};
export type CarSpec=typeof evoX;
