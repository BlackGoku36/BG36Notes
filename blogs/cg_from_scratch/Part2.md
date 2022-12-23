# Computer Graphics from scratch - 2

## Zig

In the last blog, I said that I wanted to switch from C to Zig after I have done enough C projects. After all the hard exams were over, I thought I get started with Zig with Advent of Code. At first, Zig was a bit confusing to use and took some productivity time trying to find a way to do type conversion, handling error, or even opening file. It took some days to get comfortable with Zig. And then when I got comfortable, it was a very smooth coding experience, way way better than writing C. I mean, there wasn't a time I was like 'The fook is going on !?', there were always some directions to solution.

I couldn't wait until the time was 'right' to re-write the code in Zig. So, I did it. No regrets. Zig rasterizer has a super simple (feature-wise) obj parser and textures. But it doesn't have shadow mapping as C does, which would be easy to implement, but that is not the objective at this moment. The objective is to make it fast enough for it to be interactive.

---

## Optimizations

I wanted to do some optimizations, and see how fast I can make it run before I **have** to touch SIMD or Multi-threading. Turn out, I could do a lot, lot more than I imagined. So lets get to it.

### Render-target clearing

I have two render-target, a depth buffer and a frame buffer. If I was going to make it interactive, then I would have to clear it after each frame. The code was like this, for depth-buffer:

```zig
pub fn putPixel(self: *RenderTargetR32, x: u32, y: u32, value: f32) void {
    self.buffer[y * self.width + x] = value;
}

pub fn clearColor(self: *RenderTargetR32, value: f32) void {
     var y: u32 = 0;
     var x: u32 = 0;
     while (y < self.height) : (y += 1) {
         while (x < self.width) : (x += 1) {
             self.putPixel(x, y, value);
         }
         x = 0;
     }
}
```
and for frame-buffer:

```zig
pub fn putPixel(self: *RenderTargetRGBA32, x: u32, y: u32, color: Color) void {
    self.buffer[y * 4 * self.width + (x * 4 + 0)] = color.r;
    self.buffer[y * 4 * self.width + (x * 4 + 1)] = color.g;
    self.buffer[y * 4 * self.width + (x * 4 + 2)] = color.b;
    self.buffer[y * 4 * self.width + (x * 4 + 3)] = 1.0;
}

pub fn clearColor(self: *RenderTargetRGBA32, color: Color) void {
     var y: u32 = 0;
     var x: u32 = 0;
     while (y < self.height) : (y += 1) {
         while (x < self.width) : (x += 1) {
             self.putPixel(x, y, color);
         }
         x = 0;
     }
 }
```
First thing I notice after profiling using xcode's instruments, is that this two function had high cache misses. Improving the depth-buffer was pretty simple, instead of doing all the traversal, all I did was memset the buffer. I don't remember well how much of improvement I got from this, but I think it was prolly something like

```txt
Depth-buffer size: 1280 x 720

before: ~4 ms
after: ~1 ms (or at-least small enough so profiler doesn't notice in new measurement)
```

As for frame-buffer, I couldn't do memset same way, other wise I wouldn't be able to clear it with color....or could I? It took `~19ms` to do this, which I honestly couldn't afford. And so, I memset the frame buffer too, which would give me a background with shade of grey. I think, that's ok.

```txt
Frame-buffer size: 1280 x 720

before: ~19 ms
after: ~2.5 ms
```

Which is pretty good, considering clearing buffer would itself would stop me from getting 60fps.

> **Note to reader**: I changed both of buffers type from f32 to f16 during above optimization and forgot to note how much it improved. So, 7.6x improvement for frame buffer include the type change.

> **Note to myself**: Don't forget to properly measure the performance and note it somewhere.

---

### Random things

Then I tried to optimize the code by doing random things, such making some calculation compile-time, only calculating things only one time, not making extra allocations on stack, etc. Which I haven't measure, but at best it shave off 1 or 2 ms.

---

### Back-face culling

I forgot to add this basic optimization since I first started with this project. Better late than never I guess.

Here I just took one vertice's normal and calculated dot product with camera direction, instead of using face normal. Calculating face's normal would cost me, and also that using vertice's normal looked good enough to me, so I didn't bother myself with it.

```txt
Spot model
Before back-face culling: 38.34 ms
After back-face culling: 21.885 ms
```

---

### AABB

If you have read my previous blog post, you already know that I implemented AABB, but did I do it properly here? Can you spot the blunder?

```zig
var x: u32 = aabb.min_x;
var y: u32 = aabb.min_y;
while (y <= aabb.max_y) : (y += 1) {
    while (x <= aabb.max_x) : (x += 1) {
        const xf32 = @intToFloat(f32, x);
        const yf32 = @intToFloat(f32, y);
        var w0: f32 = edgeFunction(a, b, xf32, yf32);
        var w1: f32 = edgeFunction(b, c, xf32, yf32);
        var w2: f32 = edgeFunction(c, a, xf32, yf32);
        if (windingOrderTest(winding_order, w0, w1, w2)) {
            w0 /= area;
            w1 /= area;
            w2 /= area;
            var z = 1.0 / (w1 * a.z + w2 * b.z + w0 * c.z);
            if (z < depth_buffer.getPixel(x, y)) {
                depth_buffer.putPixel(x, y, @floatCast(f16, z));
                var u = w1 * a_uv.x + w2 * b_uv.x + w0 * c_uv.x;
                var v = w1 * a_uv.y + w2 * b_uv.y + w0 * c_uv.y;
                u *= z;
                v *= z;
                u = clamp(f32, 0.0, 1.0, u);
                v = clamp(f32, 0.0, 1.0, v);
                // WHYYYYYYYYYYYYYY!!!!!!
                v = 1.0 - v;
                var tex_u = @floatToInt(u32, u * tex_width_f32);
                var tex_v = @floatToInt(u32, v * tex_height_f32);
                var albedo = texture.pixels.rgb24[tex_v * texture.width + tex_u].toColorf32();
                albedo.r *= pong;
                albedo.g *= pong;
                albedo.b *= pong;
                frame_buffer.putPixel(x, y, Color{ .r = @floatCast(f16, albedo.r), .g = @floatCast(f16, albedo.g), .b = @floatCast(f16, albedo.b) });
            }
        }
    }
    x = 0;
 }
```

<details>
    <summary>Hint!</summary>
    <p>Yeah, I want range loop in zig badly</p>
</details>

```txt
Spot model
Before: 21.885 ms
After: 4.7 ms
```

This is pretty POG (at-least to me), considering I said this in last blog.

> We will have to implement multi-threading, SIMD  and other techniques such as frustum culling, to at least make it interactive for a close-up low-poly scene.

---

### Optimizing the edge function

Improved the edge function from using 2 mults and 5 subs to simple addition as described in Scratchapixel's [Optimizin the edge function](https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/rasterization-practical-implementation). 
We get about `1.2x` improvement (spot model). But for high poly model (dragon model), we only see about `1.08x` improvement. So I don't know if it really an improvement, and if it worth having extra complexity. The problem here is that I can't properly measure improvement because I haven't written a proper `.obj` parser, and so I can't load scenes and can only do a single object test.

> **Note to myself**: Write proper .obj parser and load scene instead of single object. And also implement costy shading features to properly measure optimizations.

---

### Mesh properties data structure

The original parser I wrote followed data structure of how .obj file defined the properties:

```zig
pub const Mesh = struct {
    vertices: std.ArrayList(Vec3),
    indices: std.ArrayList(u32),

    uvs: std.ArrayList(Vec2),
    uv_indices: std.ArrayList(u32),

    normals: std.ArrayList(Vec3),
    normal_indices: std.ArrayList(u32),
    // ....
};
```

So you would have to access like:

```zig
var i: u32 = 0;
while (i < mesh.indices.items.len) : (i += 3) {
    var index1 = mesh.indices.items[i];
    var index2 = mesh.indices.items[i + 1];
    var index3 = mesh.indices.items[i + 2];

    var vert1 = mesh.vertices.items[index1];
    var vert2 = mesh.vertices.items[index2];
    var vert3 = mesh.vertices.items[index3];

    var uv_1 = mesh.uvs.items[mesh.uv_indices.items[i + 0]];
    var uv_2 = mesh.uvs.items[mesh.uv_indices.items[i + 1]];
    var uv_3 = mesh.uvs.items[mesh.uv_indices.items[i + 2]];
}
```

Which is pretty slow, as you have to do 2 array access to get to the element. Also because cache misses will be lot more likely. So I turned it into SOA (Structure-of-Array) just after parsing is done.

```zig
pub const Mesh = struct {
    vertices: std.ArrayList(Vec3),
    uvs: std.ArrayList(Vec2),
    normals: std.ArrayList(Vec3),
    indices: usize,
    // ....
};
```
```zig
var i: u32 = 0;
while (i < mesh.indices) : (i += 3) {
    var vert1 = mesh.vertices.items[i];
    var vert2 = mesh.vertices.items[i + 1];
    var vert3 = mesh.vertices.items[i + 2];

    var uv_1 = mesh.uvs.items[i];
    var uv_2 = mesh.uvs.items[i + 1];
    var uv_3 = mesh.uvs.items[i + 2];
}
```

I even tried doing AOS and AOSOA, result is:

```txt
Dragon model (high-poly)
- before: 64.965 ms
- after (SOA): 56.9 ms
- after (AOS): 59.585 ms
- after (AOSOA): 58.17 ms

Spot model (low-poly)
- before: 7.515 ms
- after (SOA): 7.32 ms
- after (AOS): -
- after (AOSOA): 7.5 ms
```

---

### Results

<div display: flex>
<video width="45%" controls>
  <source src="../assets/cg_from_scratch_part2_dragon.mov" type="video/mp4">
</video>

<video width="45%" controls>
  <source src="../assets/cg_from_scratch_part2_spot.mov" type="video/mp4">
</video>
</div>

---

### Until next time

To make sure that I don't make same mistake of not keeping note of improvements and also of not using proper test scene to measure improvement. I will create a proper `.obj` parser, and load some relatively heavy scene with materials. And also try to use PBR technique to make it even more heavy to render. And maybe even add shadows back.

After I am done with that, we will do even more optimizations :)

<details>
    <summary>P.S.</summary>
    <p>Hopefully, this has been interesting read for you :)</p>
</details>
