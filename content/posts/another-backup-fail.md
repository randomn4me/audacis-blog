+++
title = "Another Backup Fail"
description = "Or how I lost another round of pictures.. again"
date = 2025-08-24

[taxonomies]
tags = ["system administration", "backup"]
+++

I know, i know... I should have learned my lesson the first time.
But no, here I am again, having lost another round of precious pictures due to a backup failure.
And it is okay to put all the blame on myself this time (and a little "wtf" on MacOS too).

# What happened?

Yesterday I decided it would be a good time to check the privacy settings on my MacBook.
There I found, that the Apple Cloud was on full sync with every other setting.
I noticed, that the only thing synced was my iPad, but still, i did not want to risk that any of my data would be synced to the cloud.
So I disabled the sync for everything, including photos.
I assume, that there was a little popup, which asked me to delete all synced Photos on device.
As I did take some photos with my iPad, which might have been synced, I thankfully clicked "Yes".
I did not thought about the possibility, that this would go into my `$HOME/Pictures` directory and just wipe everything.

# What I tried to recover

So after I noticed my fuck-up (which was a day after), I checked all my backups, which did not work.
While I installed [nix-darwin](https://nix-darwin.github.io/nix-darwin/) on this device a month before, none of the services I configured in my flake for [home-manager](https://nix-community.github.io/home-manager/) worked, as they are built on top of [systemd](https://systemd.io/) which is not available on MacOS.
There are services in `nix-darwin` which are using [launchd](https://en.wikipedia.org/wiki/Launchd), but none for [borg](https://www.borgbackup.org/)/[borgmatic](https://torsion.org/borgmatic/).
Hence, I did not have automatic backups, yet.
As for manual backups, I regularly ran borgmatic, but my config excluded the bulky 

Then I found a Lightroom Preview file. 
But here again, there was no avail of extracting the Pictures as well.
I found a [forum](https://www.lightroomqueen.com/community/threads/recover-jpegs-from-previews-no-catalog.31930/) where extraction is discussed, but I might have been to brain-fogged at that moment to follow.

# Verdict

Nevertheless, images are gone, backup routine is in the doing (blog post will follow), and I miss the easy customizability of my system, because MacOS seems to get into the way, when doing more advanced stuff like automated backups with a script.
And be aware when turning off you iCloud backups, even when you do not use this stuff!
