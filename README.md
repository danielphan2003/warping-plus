```
  ██╗    ██╗ █████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗ ██╗     ██╗   ██╗███████╗
  ██║    ██║██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██║     ██║   ██║██╔════╝
  ██║ █╗ ██║███████║██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗    ██████╔╝██║     ██║   ██║███████╗
  ██║███╗██║██╔══██║██╔══██╗██╔═══╝ ██║██║╚██╗██║██║   ██║    ██╔═══╝ ██║     ██║   ██║╚════██║
  ╚███╔███╔╝██║  ██║██║  ██║██║     ██║██║ ╚████║╚██████╔╝    ██║     ███████╗╚██████╔╝███████║
   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝
```

![Code Size][gh-code-size] ![Top Language][gh-top-lang] ![GitHub stars][gh-stars]

- How much gore do you want this project to be?
  - Yes.

## Pretext

My brother asked me to use [warp-plus-cloudflare][warp-plus-cloudflare] for his phone, and after +1 day this happened.

## Features

Looks very cool if the one reading this right now is myself from 5 years ago. Nowadays this piece of script is just a glorified copy cat of [warp-plus-cloudflare]. Do not worry, this will soon™️ be rewritten in [Rust][rust] and exceed this script's performance with less crap.

- Auto download proxy file if not existed.
- Use cached proxy file (specify your own proxy file if needed).
- Parallel instance aka. ability to run this script multiple time (enabled by default).
- Very fast 🚀🚀🚀 (approx. _20ms per one request_, idk I just made that up).
- Very RAM hungry 🚀🚀🚀🚀 (approx. **more** than _1.1GB per instance_).

How well `warping-plus` runs depends on your proxy file size. Because it runs in parallel i.e. processing multiple proxies at once, it is best to run at **MOST** 4 instances. Of course, adjust this to your machine's performance. `warping-plus` benefits most from multi-core machines.

## Prerequisite

`pip install --user` the following:
- [httplib2][httplib2]

You also need your Warp+ ID:
- Open 1.1.1.1 App
- Click on the Hamburger Menu Icon ☰ (top left)
- Choose `Advanced` > `Diagonistics`
- Under `Client Configuration` > Copy the ID

and within `warping-plus.py` file, replace `<warp-id>` with your ID.

## Usage

### For farmers

In Linux & macOS:

```
while true; do timeout 4m "python3 ./warping-plus.py"; done
```

In Windows (I dare you use Windows for this):
```
while ($true) {
  $job = Start-Job -ScriptBlock {
    python3 ./warping-plus.py
  }
  Wait-Job $job -Timeout 4*60
  Remove-Job -force $job
}
```

### For normal users:

```
python3 ./warping-plus.py
```

[NixOS][nixos] users can just drop `python3` altogether.

### Other mobile platforms (Android, iOS):

Please, just don't.

## Acknowledgements

- [warp-plus-cloudflare][warp-plus-cloudflare] and [ALIILAPRO][ALIILAPRO] for their script and manual.
- My bro.

## Want to something interesting?

Try out [NixOS][nixos], and [DevOS][devos] please 🥺.

[gh-code-size]: https://img.shields.io/github/languages/code-size/danielphan2003/warping-plus
[gh-top-lang]: https://img.shields.io/github/languages/top/danielphan2003/warping-plus
[gh-stars]: https://img.shields.io/github/stars/danielphan2003/warping-plus

[warp-plus-cloudflare]: https://github.com/ALIILAPRO/warp-plus-cloudflare
[ALIILAPRO]: https://github.com/ALIILAPRO

[rust]: https://rust-lang.org
[httplib2]: https://github.com/httplib2/httplib2
[nixos]: https://nixos.org
[devos]: https://github.com/divnix/devos
