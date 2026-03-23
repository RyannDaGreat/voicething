"""
Flashlight mode: fullscreen EDR white overlay for maximum display brightness.

Command, specific. Creates a borderless topmost NSWindow backed by a CAMetalLayer
that renders EDR white (values > 1.0) to push the display beyond SDR brightness.
Dismissed by any key press, mouse click, or mouse movement.

Run as a standalone script:  python3 flashlight.py
Kill externally:             kill $(cat /tmp/voicething_flashlight.pid)
"""

import os
import sys
import signal
import time

# Write PID file so voice_thing can kill us
PID_FILE = '/tmp/voicething_flashlight.pid'

def _write_pid():
    """Command, specific. Write current PID to temp file for external kill."""
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def _remove_pid():
    """Command, specific. Remove PID file on exit."""
    try:
        os.remove(PID_FILE)
    except FileNotFoundError:
        pass

def _set_brightness_max():
    """Command, specific. Set display brightness to maximum via AppleScript."""
    import subprocess
    subprocess.Popen(
        "osascript -e 'tell app \"System Events\"' -e 'repeat 50 times' -e 'key code 144' -e 'delay 0.05' -e 'end repeat' -e 'end tell'",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def run_flashlight():
    """
    Command, specific. Launch fullscreen EDR white overlay.

    Creates a borderless NSWindow at CGShieldingWindowLevel backed by a
    CAMetalLayer configured for Extended Dynamic Range. Renders white at
    the display's maximum EDR headroom (~16x SDR on XDR displays).
    Exits on any keyboard, mouse click, or mouse move event.
    """
    import objc
    import ctypes
    from AppKit import (
        NSApplication, NSWindow, NSView, NSScreen, NSColor,
        NSWindowStyleMaskBorderless, NSBackingStoreBuffered,
        NSWindowCollectionBehaviorCanJoinAllSpaces,
        NSWindowCollectionBehaviorFullScreenAuxiliary,
        NSWindowCollectionBehaviorStationary,
        NSWindowCollectionBehaviorIgnoresCycle,
        NSApplicationPresentationHideDock,
        NSApplicationPresentationHideMenuBar,
        NSApplicationPresentationDefault,
        NSApplicationActivationPolicyRegular,
        NSApp,
    )
    from Quartz import (
        CAMetalLayer,
        CGColorSpaceCreateWithName,
        kCGColorSpaceExtendedLinearSRGB,
        CGShieldingWindowLevel,
    )

    # --- Metal device via ctypes (PyObjC doesn't expose MTLCreateSystemDefaultDevice directly) ---
    metal_framework = ctypes.cdll.LoadLibrary('/System/Library/Frameworks/Metal.framework/Metal')
    objc.loadBundle('Metal', globals(), bundle_path='/System/Library/Frameworks/Metal.framework')
    MTLCreateSystemDefaultDevice = metal_framework.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    device_ptr = MTLCreateSystemDefaultDevice()
    device = objc.objc_object(c_void_p=ctypes.c_void_p(device_ptr))

    # Metal constants
    MTLPixelFormatRGBA16Float = 115
    MTLLoadActionClear = 2
    MTLStoreActionStore = 1

    # --- NSApplication setup ---
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

    # --- Screen info ---
    screen = NSScreen.mainScreen()
    frame = screen.frame()
    scale = screen.backingScaleFactor()
    edr_potential = screen.maximumPotentialExtendedDynamicRangeColorComponentValue()
    print(f"[flashlight] Screen: {frame.size.width}x{frame.size.height} @ {scale}x")
    print(f"[flashlight] EDR potential headroom: {edr_potential}x")

    # --- CAMetalLayer ---
    metal_layer = CAMetalLayer.alloc().init()
    metal_layer.setDevice_(device)
    metal_layer.setPixelFormat_(MTLPixelFormatRGBA16Float)
    metal_layer.setWantsExtendedDynamicRangeContent_(True)
    metal_layer.setColorspace_(CGColorSpaceCreateWithName(kCGColorSpaceExtendedLinearSRGB))
    metal_layer.setOpaque_(True)
    metal_layer.setFramebufferOnly_(True)
    metal_layer.setContentsScale_(scale)

    # Use 1x1 drawable — we just clear-fill, no geometry needed
    metal_layer.setDrawableSize_((1, 1))

    # --- Command queue ---
    command_queue = device.newCommandQueue()

    # --- Custom NSView subclass (layer-hosting) ---
    class FlashlightView(NSView):
        pass

    content_view = FlashlightView.alloc().initWithFrame_(frame)
    content_view.setLayer_(metal_layer)
    content_view.setWantsLayer_(True)

    # --- Custom NSWindow subclass (accepts key events when borderless) ---
    _dismiss_called = [False]

    class FlashlightWindow(NSWindow):
        def canBecomeKeyWindow(self):
            return True

        def canBecomeMainWindow(self):
            return True

        def keyDown_(self, event):
            _dismiss()

        def mouseDown_(self, event):
            _dismiss()

        def mouseMoved_(self, event):
            # Ignore the very first mouseMoved — cursor warp on window creation triggers it
            if not hasattr(self, '_ignore_first_move'):
                self._ignore_first_move = True
                return
            _dismiss()

    window = FlashlightWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        NSWindowStyleMaskBorderless,
        NSBackingStoreBuffered,
        False,
    )
    window.setLevel_(CGShieldingWindowLevel())
    window.setOpaque_(True)
    window.setBackgroundColor_(NSColor.blackColor())
    window.setHasShadow_(False)
    window.setAcceptsMouseMovedEvents_(True)
    window.setReleasedWhenClosed_(False)
    window.setHidesOnDeactivate_(False)
    window.setCollectionBehavior_(
        NSWindowCollectionBehaviorCanJoinAllSpaces
        | NSWindowCollectionBehaviorFullScreenAuxiliary
        | NSWindowCollectionBehaviorStationary
        | NSWindowCollectionBehaviorIgnoresCycle
    )
    window.setContentView_(content_view)

    # --- Dismiss function ---
    def _dismiss():
        """Command, specific. Tear down the flashlight overlay and exit."""
        if _dismiss_called[0]:
            return
        _dismiss_called[0] = True
        print("[flashlight] Dismissing")
        app.setPresentationOptions_(NSApplicationPresentationDefault)
        window.orderOut_(None)
        _remove_pid()
        app.terminate_(None)

    # --- Signal handlers for external kill ---
    def _signal_handler(signum, frame):
        _dismiss()

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    # --- Show window ---
    app.setPresentationOptions_(
        NSApplicationPresentationHideDock | NSApplicationPresentationHideMenuBar
    )
    window.makeKeyAndOrderFront_(None)
    app.activateIgnoringOtherApps_(True)

    # --- Render loop: clear to EDR white ---
    # EDR headroom ramps up over ~2-3 seconds, so we render continuously
    # for a few seconds then switch to a slow idle render to maintain it.
    from Foundation import NSDate, NSDefaultRunLoopMode
    from AppKit import NSAnyEventMask

    MTLRenderPassDescriptor = objc.lookUpClass('MTLRenderPassDescriptor')

    RAMP_DURATION_S = 4.0
    RAMP_INTERVAL_S = 1.0 / 30  # 30 fps during ramp
    IDLE_INTERVAL_S = 1.0       # 1 fps after ramp (just maintain EDR)
    start_time = time.time()

    def _render_frame():
        """Command, specific. Render one frame of EDR white to the Metal layer."""
        headroom = screen.maximumExtendedDynamicRangeColorComponentValue()
        drawable = metal_layer.nextDrawable()
        if drawable is None:
            return

        pass_desc = MTLRenderPassDescriptor.renderPassDescriptor()
        color_att = pass_desc.colorAttachments().objectAtIndexedSubscript_(0)
        color_att.setTexture_(drawable.texture())
        color_att.setLoadAction_(MTLLoadActionClear)
        color_att.setStoreAction_(MTLStoreActionStore)
        # Clear to EDR white at current headroom
        color_att.setClearColor_((headroom, headroom, headroom, 1.0))

        cmd_buf = command_queue.commandBuffer()
        encoder = cmd_buf.renderCommandEncoderWithDescriptor_(pass_desc)
        encoder.endEncoding()
        cmd_buf.presentDrawable_(drawable)
        cmd_buf.commit()

    def _drain_events():
        """Command, specific. Pump NSApplication event queue so keyDown/mouseDown/mouseMoved fire."""
        while True:
            event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                NSAnyEventMask,
                NSDate.distantPast(),  # non-blocking
                NSDefaultRunLoopMode,
                True,
            )
            if event is None:
                break
            app.sendEvent_(event)
        app.updateWindows()

    # Main run loop with rendering
    print("[flashlight] Starting EDR render loop")
    while not _dismiss_called[0]:
        elapsed = time.time() - start_time
        interval = RAMP_INTERVAL_S if elapsed < RAMP_DURATION_S else IDLE_INTERVAL_S

        _render_frame()
        _drain_events()

        # Sleep to control frame rate (avoid busy-spinning)
        time.sleep(interval)


if __name__ == '__main__':
    _write_pid()
    try:
        _set_brightness_max()
        run_flashlight()
    finally:
        _remove_pid()
