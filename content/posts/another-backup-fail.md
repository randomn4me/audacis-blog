+++
title = "Another Backup Fail"
description = "Or how I lost another round of pictures.. again"
date = 2025-08-24

[taxonomies]
tags = ["sysadmin", "backup"]
+++

I know, I know... I should have learned my lesson the first time.
But no, here I am again, having lost another round of precious pictures due to a backup failure.
And it is okay to put all the blame on myself this time (and a tiny "wtf" on MacOS too).

# What happened?

Yesterday I decided it would be a good time to check the privacy settings on my MacBook.
I found that the Apple Cloud completely synced with every other setting.
I noticed that the only thing synced was my iPad, but still, I did not want to risk that any of my data would be synced to the cloud.
So I disabled the sync for everything, including photos.
There was a little pop-up, which asked me to delete all synced Photos on the device.
As I did take some photos with my iPad, which might have been synced, I thankfully clicked "Yes".
I did not think about the possibility that this would go into my `$HOME/Pictures` directory and just wipe everything.

# What I tried to recover

So after I noticed my fuck-up (which was a day after), I checked all my backups, which did not work.
While I installed [nix-darwin](https://nix-darwin.github.io/nix-darwin/) on this device a month before, none of the services I configured in my flake for [home-manager](https://nix-community.github.io/home-manager/) worked, as they are built on top of [systemd](https://systemd.io/), which is not available on macOS.
There are services in `nix-darwin` which are using [launchd](https://en.wikipedia.org/wiki/Launchd), but none for [borg](https://www.borgbackup.org/)/[borgmatic](https://torsion.org/borgmatic/).
Hence, I did not have automatic backups yet.
As for manual backups, I regularly ran borgmatic, but my config excluded the bulky files such as videos and raw images (CR2 and CR3).

Then I found a Lightroom Preview file. 
But here again, I was not able to extract the pictures either.
I found a [forum](https://www.lightroomqueen.com/community/threads/recover-jpegs-from-previews-no-catalog.31930/) where extraction is discussed, but I might have been too brain-fogged at that moment to follow.

# Verdict

Nevertheless, my images are gone, the backup routine is in the works (the blog post will follow), and I miss the easy customizability of my system, because macOS seems to get in the way when doing more advanced stuff like automated backups with a script.
Be aware of this when turning off your iCloud backups, even when you do not use this stuff!

