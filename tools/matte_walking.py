"""Create the hero's packed RGB/alpha videos without modifying the source.
Requires rembg, onnxruntime, numpy, Pillow, scipy and ffmpeg.
"""
import json
import subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from rembg import new_session, remove

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'public/media'
W, H, FPS = 720, 1280, 24

def main():
    session = new_session('u2net', providers=['CPUExecutionProvider'])
    decoder = sp.Popen(['ffmpeg','-v','error','-i',str(MEDIA/'me_walking.webm'),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=sp.PIPE)
    encoders = []
    for ext, codec in [('mp4',['-c:v','libx264','-preset','fast','-crf','18','-movflags','+faststart']),('webm',['-c:v','libvpx-vp9','-b:v','0','-crf','24','-cpu-used','4'])]:
        encoders.append(sp.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W*2}x{H}','-r',str(FPS),'-i','-','-i',str(MEDIA/'me_walking.webm'),'-map','0:v:0','-map','1:a:0','-c:a',('aac' if ext=='mp4' else 'libopus'),'-shortest',*codec,'-pix_fmt','yuv420p',str(MEDIA/f'me_walking_clean.{ext}')],stdin=sp.PIPE))
    boxes=[]
    i=0
    while True:
        raw=decoder.stdout.read(W*H*3)
        if not raw: break
        if len(raw)!=W*H*3: raise RuntimeError('Incomplete video frame')
        rgb=np.frombuffer(raw,np.uint8).reshape(H,W,3)
        # Erase the white stand-in BEFORE inference so its outline does not
        # cause the model to retain attached studio background by the legs.
        white=(rgb.min(2)>165)&(np.ptp(rgb.astype(np.int16),axis=2)<55)
        white_labels,_=ndi.label(white)
        white_sizes=np.bincount(white_labels.ravel()); white_sizes[0]=0
        yy=np.arange(H)[:,None]
        white &= (white_sizes[white_labels]>60)|((yy>450)&(yy<950))
        white=ndi.binary_dilation(white,iterations=3)
        clean=rgb.copy(); clean[white]=[8,12,14]
        alpha=np.asarray(remove(Image.fromarray(clean),session=session,only_mask=True),dtype=np.float32)/255
        alpha[white]=0
        labels,count=ndi.label(alpha>.5)
        if not count: raise RuntimeError(f'No person at frame {i}')
        sizes=np.bincount(labels.ravel()); sizes[0]=0
        person=ndi.binary_opening(labels==sizes.argmax(),iterations=2)
        alpha*=ndi.binary_dilation(person,iterations=1)
        # Suppress uncertain background coverage without a wide blurred halo.
        alpha=np.clip((alpha-.12)/.8,0,1)
        ys,xs=np.where(alpha>.35)
        boxes.append([float(xs.min()/W),float(ys.min()/H),float((xs.max()+1)/W),float((ys.max()+1)/H)])
        packed=np.concatenate([(rgb*alpha[:,:,None]).astype(np.uint8),np.repeat((alpha*255).astype(np.uint8)[:,:,None],3,axis=2)],axis=1)
        for encoder in encoders: encoder.stdin.write(packed.tobytes())
        if i==96: Image.fromarray(packed).save(MEDIA/'me_walking_clean.jpg',quality=95)
        if i in [0,48,96,144,192,239]:
            bg=np.zeros_like(rgb); bg[:]=[105,35,40]
            Image.fromarray((rgb*alpha[:,:,None]+bg*(1-alpha[:,:,None])).astype(np.uint8)).save(f'/private/tmp/walking-qa-{i}.jpg')
        i+=1
        if i%24==0: print(f'{i}/240 frames',flush=True)
    if decoder.wait(): raise RuntimeError('Decoder failed')
    for encoder in encoders:
        encoder.stdin.close()
        if encoder.wait(): raise RuntimeError('Encoder failed')
    arr=np.array(boxes); pad=np.pad(arr,((4,4),(0,0)),mode='edge')
    track=np.stack([np.convolve(pad[:,j],np.ones(9)/9,'valid') for j in range(4)],axis=1).round(4).tolist()
    path=MEDIA/'manifest.json'; manifest=json.loads(path.read_text())
    manifest['clips']['hero'].update(webm='me_walking_clean.webm',mp4='me_walking_clean.mp4',poster='me_walking_clean.jpg',format='packed',packed=True,w=W,h=H,frames=i,track=track)
    path.write_text(json.dumps(manifest,indent=1)+'\n')
    print('Packed videos and hero manifest updated.',flush=True)

if __name__=='__main__': main()
