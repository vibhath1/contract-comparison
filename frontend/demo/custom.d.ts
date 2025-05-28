import * as THREE from 'three';
import { ShaderMaterial } from 'three';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      particleGlowMaterial: ReactThreeFiber.Object3DNode<ShaderMaterial, typeof ShaderMaterial>;
    }
  }
}
