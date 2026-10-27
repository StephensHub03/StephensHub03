import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func read(_ path: String) -> CGImage {
 let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil)!
 return CGImageSourceCreateImageAtIndex(source, 0, nil)!
}
let base = read("tmp/face-edit/before.png")
let face = read("public/media/skillme.jpeg")
let w = base.width, h = base.height
let space = CGColorSpaceCreateDeviceRGB()
let info = CGImageAlphaInfo.premultipliedLast.rawValue
let context = CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:space,bitmapInfo:info)!
context.draw(base,in:CGRect(x:0,y:0,width:w,height:h))
let overlay = CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:space,bitmapInfo:info)!
// Only uniform resizing and placement; no color or facial transformations.
let scale = 0.60, tx = 240.0, ty = -43.0
overlay.interpolationQuality = .high
overlay.draw(face,in:CGRect(x:tx,y:Double(h)-ty-Double(face.height)*scale,width:Double(face.width)*scale,height:Double(face.height)*scale))
let outline: [(Double,Double)] = [(491,391),(500,351),(523,337),(558,337),(585,355),(622,377),(650,405),(674,432),(709,436),(729,455),(732,484),(715,514),(690,534),(677,557),(680,590),(674,636),(659,679),(644,706),(619,727),(605,718),(584,698),(568,663),(549,626),(536,602),(533,579),(525,555),(516,533),(510,511),(502,492),(497,472),(493,450),(490,427)]
let polygon = outline.map { (tx+$0.0*scale,ty+$0.1*scale) }
func inside(_ x:Double,_ y:Double)->Bool {
 var yes=false; var j=polygon.count-1
 for i in polygon.indices { let a=polygon[i], b=polygon[j]
  if ((a.1>y) != (b.1>y)) && x < (b.0-a.0)*(y-a.1)/(b.1-a.1)+a.0 {yes.toggle()};j=i
 };return yes
}
let dest=context.data!.assumingMemoryBound(to:UInt8.self)
let src=overlay.data!.assumingMemoryBound(to:UInt8.self)
for y in 150..<400 {for x in 525..<685 {
 let px=Double(x)+0.5, py=Double(y)+0.5
 guard inside(px,py) else {continue}
 var distance=Double.infinity
 for i in polygon.indices {let a=polygon[i],b=polygon[(i+1)%polygon.count];let dx=b.0-a.0,dy=b.1-a.1
 let t=max(0,min(1,((px-a.0)*dx+(py-a.1)*dy)/(dx*dx+dy*dy)))
 distance=min(distance,hypot(px-a.0-t*dx,py-a.1-t*dy))
 }
 // Soften only the narrow cut edge; face interior retains source colors.
 let feather = py > 305 ? 4.0 : (px < 565 && py > 255 ? 1.8 : 6.0)
 let alpha=min(1,distance/feather), offset=(y*w+x)*4
 for c in 0..<3 {dest[offset+c]=UInt8((Double(src[offset+c])*alpha+Double(dest[offset+c])*(1-alpha)).rounded())}
}}
let result=context.makeImage()!
let output=CGImageDestinationCreateWithURL(URL(fileURLWithPath:"public/skills/skillme-desk-scene.png") as CFURL,UTType.png.identifier as CFString,1,nil)!
CGImageDestinationAddImage(output,result,nil)
assert(CGImageDestinationFinalize(output))
