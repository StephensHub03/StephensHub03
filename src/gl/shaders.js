// GLSL for the hero compositor.
//
// Every clip arrives "packed": the left half of the video frame is premultiplied
// colour, the right half is the alpha matte. Unpacking here is what gives real
// per-pixel transparency in every browser, including Safari, which supports
// neither WebM alpha nor HEVC alpha on Windows-encoded files.

export const VERT = `#version 300 es
precision highp float;
layout(location=0) in vec2 aPos;          // unit quad 0..1
uniform vec4 uRect;                        // x, y, w, h in pixels
uniform vec2 uRes;
uniform vec4 uUV;                          // sub-rect in the source texture
uniform vec2 uSkew;                        // parallax / drift offset in pixels
out vec2 vUV;
out vec2 vLocal;
out vec2 vScreen;
void main(){
  vLocal = aPos;
  vUV = uUV.xy + aPos * uUV.zw;
  vec2 px = uRect.xy + aPos * uRect.zw + uSkew;
  vScreen = px / uRes;
  vec2 clip = vec2(px.x / uRes.x * 2.0 - 1.0, 1.0 - px.y / uRes.y * 2.0);
  gl_Position = vec4(clip, 0.0, 1.0);
}`;

// --------------------------------------------------------------------------
// Background: not a flat fill. A flat #000 reads as "screen off"; the reference
// art has a faint mottled black, so the plate gets a low-amplitude texture, a
// deep vignette and a slow red ember behind the wordmark.
// --------------------------------------------------------------------------
export const FRAG_BG = `#version 300 es
precision highp float;
in vec2 vScreen;
uniform sampler2D uFloor;
uniform float uEmber;
uniform float uAspect;
uniform float uTime;
out vec4 frag;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
    mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0)), f.x), f.y);
}
float mist(vec2 p) {
  return noise(p) * 0.57 + noise(p * 2.03) * 0.28 + noise(p * 4.07) * 0.15;
}
void main(){
  vec2 p = vScreen;
  vec2 uv = p;
  uv.x = 0.5 + (uv.x - 0.5) * min(1.0, uAspect / 1.5);
  uv.y = uv.y < 0.77 ? uv.y * (0.70 / 0.77)
    : 0.70 + (uv.y - 0.77) * (0.30 / 0.23);

  // Advect the haze upward, anchored at the horizon. The floor stays still.
  float above = 1.0 - smoothstep(0.735, 0.77, p.y);
  float hazeMask = above * smoothstep(0.25, 0.64, p.y);
  vec2 flow = vec2(mist(vec2(uv.x * 7.0, uv.y * 5.0 + uTime * 0.22)),
    mist(vec2(uv.x * 6.0 + 9.0, uv.y * 7.0 + uTime * 0.3)));
  vec2 movingUV = uv + (flow - 0.5) * vec2(0.065, 0.085) * hazeMask;
  vec3 col = texture(uFloor, movingUV).rgb;

  // Broad volumetric shafts drift independently through rising turbulent mist.
  // Their soft boundaries avoid the appearance of rigid laser beams.
  float rise = max(0.0, 0.77 - p.y);
  float x = (p.x - 0.5) * min(uAspect, 1.6);
  float cloud = mist(vec2(x * 8.0 + uTime * 0.055, rise * 11.0 - uTime * 0.32));
  float rays = 0.0;
  for (int i = 0; i < 5; i++) {
    float fi = float(i);
    float spread = (fi - 2.0) * 0.48 + sin(uTime * 0.23 + fi * 1.7) * 0.24;
    float center = rise * spread + sin(uTime * 0.31 + fi * 2.3) * 0.018;
    float width = 0.018 + rise * 0.095;
    float ray = exp(-pow((x - center) / width, 2.0));
    rays += ray * (0.65 + 0.35 * sin(uTime * 0.6 + fi * 1.9));
  }
  float heightFade = exp(-rise * 6.0) * smoothstep(0.0, 0.045, rise);
  col += vec3(0.34, 0.027, 0.012) * rays * cloud * heightFade * above;
  col *= 1.0 + (cloud - 0.5) * hazeMask * 0.45;

  // The moving light catches existing puddles without sliding the surface.
  float floorMask = smoothstep(0.77, 0.8, p.y);
  float shimmer = sin(uTime * 1.15 + p.y * 42.0 + noise(vec2(p.x * 13.0, uTime * 0.12)) * 5.0);
  col *= 1.0 + shimmer * 0.13 * floorMask;
  frag = vec4(col * uEmber, 1.0);
}`;

// --------------------------------------------------------------------------
// Letter: glyph coverage from the word atlas, surfaced with the distressed
// texture lifted from the supplied artwork, and revealed by a directional
// dissolve rather than a plain opacity fade.
// --------------------------------------------------------------------------
export const FRAG_LETTER = `#version 300 es
precision highp float;
in vec2 vUV;
in vec2 vLocal;
in vec2 vScreen;
uniform sampler2D uGlyph;
uniform sampler2D uGrunge;
uniform vec2  uGrungeScale;
uniform vec2  uGrungeOffset;
uniform vec3  uInk;
uniform float uOpacity;
uniform float uReveal;      // 0..1 dissolve
uniform float uSoften;      // simulated defocus while materialising
uniform float uEdgeLight;
uniform float uWear;        // how distressed the paint is
uniform float uWearGain;    // contrast of the wear pattern
out vec4 frag;

// Directional smear along the axis the letter is travelling. Blurring in x too
// would sample the NEIGHBOURING letter out of the shared atlas and ghost it into
// this one; a vertical-only smear is also the honest read of a rising object.
float glyph(vec2 uv, float r){
  if(r < 0.0002) return texture(uGlyph, uv).r;
  float a = texture(uGlyph, uv).r * 0.30;
  a += texture(uGlyph, uv + vec2(0.0,  r      )).r * 0.20;
  a += texture(uGlyph, uv + vec2(0.0, -r      )).r * 0.20;
  a += texture(uGlyph, uv + vec2(0.0,  r * 2.1)).r * 0.15;
  a += texture(uGlyph, uv + vec2(0.0, -r * 2.1)).r * 0.15;
  return a;
}

void main(){
  float cov = glyph(vUV, uSoften);
  if(cov <= 0.001) discard;

  // Two octaves of the same worn plate: a coarse one for blotching and abrasion,
  // a fine one for the scratches. Sampled in SCREEN space, so it reads as one
  // continuous distressed sheet lying across the whole wordmark.
  vec2 gu = vScreen * uGrungeScale + uGrungeOffset;
  float tex = texture(uGrunge, gu).r;
  float tex2 = texture(uGrunge, gu * 3.1 + vec2(0.37, 0.11)).r;
  float wear = mix(tex, tex2, 0.42);
  wear = clamp((wear - 0.5) * uWearGain + 0.5, 0.0, 1.0);

  // the artwork red is not flat: scratches drop it toward a dried oxblood, and
  // the untouched paint sits a little hotter than the base ink
  vec3 col = uInk * mix(1.0 - uWear, 1.0 + uWear * 0.30, wear);
  col = mix(col, uInk * vec3(0.42, 0.30, 0.30),
            smoothstep(0.30, 0.02, wear) * uWear * 1.2);

  // a hair of lift along the top of each stroke, as if lit from above
  float lift = smoothstep(0.0, 0.22, 1.0 - vLocal.y);
  col += uInk * lift * uEdgeLight * 0.28;

  // A raking light gives the worn red face depth, with a dark lower edge.
  float relief = texture(uGrunge, gu + vec2(0.0015, -0.002)).r - tex;
  col *= mix(1.14, 0.48, smoothstep(0.3, 1.0, vLocal.y));
  col += vec3(0.7, 0.09, 0.035) * relief * 1.8;
  float bevel = max(0.0, cov - glyph(vUV + vec2(0.0008, 0.0012), 0.0));
  col += vec3(0.6, 0.07, 0.04) * bevel;

  // dissolve: threshold the texture so the letter emerges in flecks rather than
  // fading uniformly. n is the "appears last" field - low n surfaces first, so
  // the letter builds from its base upward through the worn grain.
  float n = wear * 0.55 + vLocal.y * 0.45;
  float m = clamp((uReveal * 1.4 - n) / 0.4, 0.0, 1.0);
  float a = cov * uOpacity * m;

  frag = vec4(col * a, a);
}`;

// --------------------------------------------------------------------------
// Figure: unpack colour+matte, grade it into the scene, optionally clip it to a
// glyph so the person genuinely lives inside a letter.
// --------------------------------------------------------------------------
export const FRAG_FIGURE = `#version 300 es
precision highp float;
in vec2 vUV;
in vec2 vLocal;
in vec2 vScreen;
uniform sampler2D uClip;      // packed video
uniform float uPacked;       // 1: colour + matte halves, 0: regular video
uniform sampler2D uGrunge;
uniform sampler2D uMask;      // glyph coverage, when clipping into a letter
uniform vec4  uMaskUV;
uniform float uUseMask;
uniform float uOpacity;
uniform float uReveal;
uniform float uFeetFade;      // dissolve the floor contact into darkness
uniform float uTopFade;
uniform float uExposure;
uniform float uLift;          // shadow lift toward cool blue
uniform float uRimRed;        // bounce from the red typography
uniform float uContrast;
uniform float uDesat;
uniform vec2  uTexel;
uniform float uFloorY;        // frame-space start of the glossy-floor band
uniform vec2  uBand;          // wordmark cap-top / baseline in screen space
out vec4 frag;

// uv arrives in FRAME space (0..1 over the source video). That lets a figure be
// drawn on a quad that is not its own rectangle - which is exactly what putting
// a person inside a letter requires: the quad is the glyph, the sampling is his.
vec4 sampleClip(vec2 uv){
  if(uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) return vec4(0.0);
  if(uPacked < 0.5) {
    vec3 col = texture(uClip, uv).rgb;
    // Regular footage has no matte. Feather only its frame edges; preserve
    // the supplied video's content instead of reading its right half as alpha.
    float edge = smoothstep(0.0, 0.1, uv.x) * smoothstep(0.0, 0.1, 1.0-uv.x)
      * smoothstep(0.0, 0.1, uv.y) * smoothstep(0.0, 0.1, 1.0-uv.y);
    return vec4(col * edge, edge);
  }
  // colour occupies the left half, matte the right; inset by a texel so chroma
  // subsampling across the seam cannot bleed one into the other
  vec2 c = vec2(clamp(uv.x * 0.5, uTexel.x, 0.5 - uTexel.x), uv.y);
  vec3 col = texture(uClip, c).rgb;
  float a = texture(uClip, c + vec2(0.5, 0.0)).r;
  return vec4(col, a);
}

void main(){
  vec4 s = sampleClip(vUV);
  float a = s.a;
  if(a <= 0.004) discard;
  vec3 col = s.rgb / max(a, 0.06);        // undo premultiply before grading

  // --- grade -------------------------------------------------------------
  float l = dot(col, vec3(0.2126, 0.7152, 0.0722));
  col = mix(vec3(l), col, 1.0 - uDesat);
  col = (col - 0.5) * uContrast + 0.5;
  col *= uExposure;
  col += vec3(0.010, 0.014, 0.030) * uLift * (1.0 - smoothstep(0.0, 0.5, l));

  // Red bounce from the wall of type behind him. Keyed off the MATTE, not the
  // quad, so it lands as a rim light on his actual silhouette - and gated to
  // the rows where the wordmark actually sits behind him. A red edge on his
  // shins, below the baseline where there is only blackness, reads as a fault.
  float edge = 1.0 - smoothstep(0.20, 0.90, s.a);
  float behindType = smoothstep(uBand.x - 0.04, uBand.x + 0.03, vScreen.y)
                   * (1.0 - smoothstep(uBand.y - 0.02, uBand.y + 0.05, vScreen.y));
  col += vec3(0.80, 0.10, 0.11) * uRimRed * edge * mix(0.12, 1.0, behindType);

  col = max(col, vec3(0.0));

  // --- coverage ----------------------------------------------------------
  if(uUseMask > 0.5){
    vec2 mu = uMaskUV.xy + vLocal * uMaskUV.zw;
    a *= texture(uMask, mu).r;
  }
  a *= smoothstep(0.0, uFeetFade, 1.0 - vLocal.y);
  a *= smoothstep(0.0, uTopFade, vLocal.y);

  // Glossy-floor band of the source frame. Reflections and specular smears
  // around the shoes survive the key with high alpha, so gating coverage alone
  // cannot remove them - they are bright PIXELS, not soft edges. The band is
  // therefore also driven down toward black, which both kills the halo and
  // reads correctly: he is standing in darkness, not on a lit studio floor.
  if(uFloorY < 1.0 && vUV.y > uFloorY){
    float depth = clamp((vUV.y - uFloorY) / max(1.0 - uFloorY, 1e-3), 0.0, 1.0);
    a *= mix(1.0, smoothstep(0.40, 0.82, a), min(depth * 1.6, 1.0));
    col *= mix(1.0, 0.10, smoothstep(0.0, 0.95, depth));
  }

  float n = texture(uGrunge, vLocal * vec2(1.7, 0.9) + vec2(0.13, 0.41)).r;
  float field = n * 0.45 + (1.0 - vLocal.y) * 0.55;   // surfaces feet-first
  a *= clamp((uReveal * 1.4 - field) / 0.4, 0.0, 1.0) * uOpacity;

  frag = vec4(col * a, a);
}`;

// --------------------------------------------------------------------------
// Contact shadow. The single cheapest thing that stops a keyed figure looking
// pasted on: some darkness that belongs to him, falling on what is behind him.
// --------------------------------------------------------------------------
export const FRAG_SHADOW = `#version 300 es
precision highp float;
in vec2 vLocal;
uniform float uOpacity;
uniform vec2  uFalloff;   // horizontal, vertical softness
out vec4 frag;
void main(){
  vec2 d = (vLocal - vec2(0.5, 1.0)) / uFalloff;
  float a = exp(-dot(d, d) * 3.0) * uOpacity;
  // Fade before the quad boundary; clipping the peak at y=1 leaves a dark box.
  a *= smoothstep(0.0, 0.12, vLocal.x)
     * smoothstep(0.0, 0.12, 1.0 - vLocal.x)
     * smoothstep(0.0, 0.22, 1.0 - vLocal.y);
  frag = vec4(0.0, 0.0, 0.0, clamp(a, 0.0, 1.0));
}`;

// --------------------------------------------------------------------------
// Final pass: grain, a breath of bloom on the reds, and the vignette.
// --------------------------------------------------------------------------
export const FRAG_POST = `#version 300 es
precision highp float;
in vec2 vScreen;
uniform sampler2D uGrain;
uniform vec2 uRes;
uniform float uTime;
uniform float uAmount;
uniform float uAspect;
uniform float uFlash;
out vec4 frag;
void main(){
  vec2 p = vScreen;
  vec2 jitter = vec2(fract(sin(uTime * 12.9898) * 43758.5453),
                     fract(sin(uTime * 78.233) * 12345.6789));
  float g = texture(uGrain, p * (uRes / 512.0) + jitter).r - 0.5;
  vec2 v = (p - 0.5) * vec2(uAspect, 1.0);
  float vig = smoothstep(0.42, 1.2, length(v));
  vec3 col = vec3(g * uAmount);
  col += vec3(0.085, 0.008, 0.011) * uFlash;
  frag = vec4(col, vig * 0.55 + uFlash * 0.1);
}`;
