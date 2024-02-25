import Slate.slate as slate

site = slate.Site()
site.name = "URJASVI SUTHAR"
site.description = '''Hi, I am Urjasvi Suthar (BlackGoku36), a 3rd-year undergraduate student at IIIT Sri City, India.
I am interested in building compilers and exploring different concepts under system software umbrella.
Previously, I had made lot of projects in computer graphics's area.
Other than coding, I like reading books from different genres such as fantasy, thriller and self-help.'''
site.picture = "pfp.png"

site.blogs.append(slate.Blog("Slate, a static site generator", "Slate.md", False))

cg_series = slate.Series("Computer Graphics from scratch", [])
cg_series.blogs.append(slate.Blog("Part - 1 | Basics Implementation", "cg_from_scratch/Part1.md", False))
cg_series.blogs.append(slate.Blog("Part - 2 | Optimizations", "cg_from_scratch/Part2.md", False))
site.blogs.append(cg_series)

wasm_series = slate.Series("WebAssembly (WASM)", [])
wasm_series.blogs.append(slate.Blog("Introduction", "wasm/intro.md", True))
site.blogs.append(wasm_series)

site.blogs.append(slate.Blog("Cache Memory", "CacheMemory.md", True))

site.contacts.append(slate.Contact.github("https://github.com/BlackGoku36"))
site.contacts.append(slate.Contact.twitter("https://twitter.com/UrjasviS"))
site.contacts.append(slate.Contact.mastodon("https://mastodon.gamedev.place/@UrjasviSuthar"))
site.contacts.append(slate.Contact.mail("urjasvisuthar@gmail.com"))
site.copyright = "© 2021-2023 Urjasvi Suthar"
slate.generate_site(site)
