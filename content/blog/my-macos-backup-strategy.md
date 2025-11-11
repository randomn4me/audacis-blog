+++
title = "My MacOS Backup Strategy"
description = "When you want to use custom tooling instead of something like time machine"
date = 2025-09-12

[taxonomies]
tags = ["macos", "backup", "sysadmin", ]
+++

As outlined in my last [blog post](posts/another-backup-fail), I failed at my backups again[^1], which led me to setting up [`borgmatic`](https://torsion.org/borgmatic/) again.
It is a wrapper for the fantastic tool [borg](https://www.borgbackup.org/), a command-line tool to create incremental backups of your system.
Like every other power-user tool, `borgmatic` is highly configurable, can back up to different repositories (storage backends) simultaneously, and does automated checks and pruning to keep just the essential bits.
However, this should not be an advertisement post about this tool.
I want to give an overview of what I want to set up, how I configured it, and what to look for when running custom services on macOS.
You find a summary at the bottom of this post.

## The Goal

Every backup strategy should follow at least the 3-2-1 rule:
- 3 copies
- 2 storage backends
- 1 off-site backup

This is accomplished by having *a storage disk at home* for backups and *one storage server*.
With this in mind, I want to set up a remote backup repository (to stay within the naming of borg) and a local, attachable drive for my backups.
My system should run `borg` every 10 minutes, whether the repository is currently available.
Ultimately, I want to receive an error if both repositories are unavailable during a run. I usually do not work from home, where my backup drive sits.

## The Setup

As for the storage server, I already used [Hetzner's storage box](https://www.hetzner.com/storage/storage-box?country=us), which is nearly a steal for remote backups that you do not want to host.
They go for 3.2 €/TB to 2.03 €/TB per month, depending on your tier (08/2025), and provide server RAID redundancy.
You could order two in different locations (1 in Germany and 1 in Finland).
After you decide on the tier you require, you:
1) Set up the access: either via SSH (which allows `rsync` and `borg`), WebDAV, or ftp,
2) setup your SSH key (`ssh-keygen && cat ~/.ssh/id_ed25519.pub`), and
3) Set your box to externally accessible, and that's it.
All done in less than 2 minutes.

My local backup drive is already available.
I back up my Linux system with it regularly and automatically with `borgmatic`, which is attached via my monitor at home.
In addition, I plan to set up my Raspberry Pi with an m.2 hat to serve as a backup server, but that is a to-do for me in the future.

With my two repositories available, I need to configure `borgmatic`.
I adjusted my Linux config, resulting in the config below (comments included for explanations and are prefixed with `#`) stored at `$HOME/.config/borgmatic/config.yaml`.

```
# the directories to backup
source_directories:
    - /Users/pkuehn/Documents
    - /Users/pkuehn/Movies
    - /Users/pkuehn/Music
    - /Users/pkuehn/Pictures
    - /Users/pkuehn/src       # all my source code
    - /Users/pkuehn/var       # stuff

repositories:       # defines the repos, labels are for internal references
    - path: user@storagbox:23/path/to/repo/dir      # url with path
      label: storagebox
    - path: user@storagbox:23/path/to/repo/dir      # url with path
      label: storagebox-helsiki

archive_name_format: "macbook-{now:%Y-%m-%dT%H:%M:%S.%f}"

keep_hourly: 12
keep_daily: 15
keep_weekly: 8
keep_monthly: 6
keep_yearly: 4

exclude_patterns:
    - '*.pyc'
    - '**/.cache'
    - '**/.venv'                # python virtual env
    - '**/.devenv'              # devenv (awesome tool)
    - 'src/**/target' # exclude these big rust dirs
    - 'Music/Music              # just a copy of everything else in the music dir

match_archives: '*'

exclude_caches: true

exclude_if_present:
    - .nobackup                 # excludes all dirs with a hidden file `.nobackup`
                                # while I do not like this ad hoc exclusion
                                # it just works

checks:                         # define regular consistency checks
    - name: repository
    - name: archives
      frequency: 1 week

encryption_passcommand: 'your pass command'  # a command, which returns your password
ssh_command: 'your ssh command'              # your ssh key, with the keyfile
                                             #   option for your storage box
relocated_repo_access_is_ok: true            # don't complain if repo moves
```

With this in place, I need to set up the repositories for this backup with `borgmatic init --encryption repo-key`, which initializes the repos.
Afterward, you run `borgmatic key export` to extract the repo-keys and store them in your password store.
Now you can confirm `borgmatic` is working by running it and waiting a long time for no feedback (`borgmatic` is a little weird in this regard, as it does not return any feedback if not using any verbose parameter, unlike `borg`, which outputs everything).

## Custom Services on MacOS

Coming from Linux, I used tools like cron or systemd a lot.
Both offer ways to run scripts or tools regularly, with cron being the standard since the beginning of Linux, and systemd being the *new* horse in town since 2010.
On macOS, however, cron is deprecated and systemd is not available.
MacOS uses a scheduler, LaunchD, which defines services in an XML format.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>backup-service</string>
        <key>Program</key>
        <string>/opt/homebrew/bin/borgmatic</string>
        <key>RunAtLoad</key>
        <true/>
    </dict>
</plist>
```

This service definition is labeled `backup-service`, and starts the program `/opt/homebrew/bin/borgmatic` on load.
And that's it.
It runs the service just once.
Depending on where you store it, it runs with different scopes.
[launchd.info](https://launchd.info/) provides an overview of launchd services with [this manpage](https://manpagez.com/man/5/launchd.plist/) giving a more comprehensive overview.
The interesting bits for me are:
- how to start services with a timer logic (similar to [systemd-timers](https://wiki.archlinux.org/title/Systemd/Timers) or cron jobs)
- How to adhere to the macOS power management, as I guessed, there will be a fancy flag for that as well in this user-friendly operating system
- How to handle a short interval, but no overlapping of service starts. `borg` (or `borgmatic`) blocks overlapping runs, but maybe there is a way to disable this in the service definition as well

Starting the service was the easiest part.
You can specify a `StartInterval` as follows.

```xml
<key>StartInterval</key>
<integer>600</integer>      # seconds (10mins here)
```

If interested, you could even start the service at a specific time of day with `StartCalendarInterval`, similar to `crontab's.
But a simple `*/5 1 * * *` like you would have done in cron, which specifies to run the command every five minutes during the second hour of the day, requires you to write the following XML [^2]:

```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Minute</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>5</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>10</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>15</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>20</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>25</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>30</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>35</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>40</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>45</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>50</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
    <dict>
        <key>Minute</key>
        <integer>55</integer>
        <key>Hour</key>
        <integer>1</integer>
    </dict>
</array>
```

Hence, I wrote a [simple Python tool](https://github.com/randomn4me/crontab-to-launchd) to convert crontab entries to simple launchd entries.
It does not add any fuzz or fancy, but it should suffice for a starter and for configuring later.
But back to the topic.

The second part I was interested in was service power management settings.
Here I found information in [the launchd.plist (5) manual](https://manpagez.com/man/5/launchd.plist/) and [this launchctl (1) manual](https://manpagez.com/man/1/launchctl/).
The vital flag is `LimitLoadToSessionType`

```txt
LimitLoadToSessionType <string>
This configuration file only applies to sessions of the type specified.
This key is used in concert with the `-S` flag to `launchctl`.
```

with the launchctl sessiontype being *Aqua*, *LoginWindow*, *Background*, *StandardIO*, and *System*.

```txt
-S sessiontype
       Some jobs only make sense in certain contexts. This
       flag instructs launchctl to look for jobs in a differ-
       ent location when using the -D flag, and allows
       launchctl to restrict which jobs are loaded into which
       session types. Currently known session types include:
       Aqua, LoginWindow, Background, StandardIO and System.
```

[This documentation](https://developer.apple.com/library/archive/technotes/tn2083/_index.html#//apple_ref/doc/uid/DTS10003794-CH1-SUBSECTION3) provides a comprehensive overview of the former four session types.
The *System* type seems not to be documented at all (according to [this mailing list](https://launchd-dev.macosforge.narkive.com/jvjz3d0r/launchd-system-session-type)), so I copied what is written in the mailing list.

- **Aqua (default):** Run app when the user is logged in. Has GUI access.
- **StandardIO:** Runs only in non-GUI login sessions (most notably, SSH login sessions).
- **Background:** Runs in a context that's the parent of all contexts for a given user.
- **LoginWindow:** Runs in the login window context.
- **System:** Services run in system/root context (requires root privileges).

The session type `System` is for root services, which I currently do not need.
~~As I want to run a `background` backup service, where the GUI is not required but should also run in the GUI session if they are up, I went for the SessionType `Background` (surprise).
This does not strictly adhere to the requirement of *power management*, such as running only when on a power adapter or Wi-Fi.~~
**Edit:** The `background` service is a system-wide service and causes problems, when used for user services.
Hence I removed the full `LimitLoadToSessionType` key.

The third part I wanted to deal with is the non-overlapping service starts.
I started out with using the following snippet:

```xml
<key>LaunchOnlyOnce</key>
    <true/>
```

After I added it to the plist file, I was surprised that it ran my *intervalled* service just once.
I checked the doc and noticed that this flag overrides any indicated interval services.
Fair point, so I removed this flag and let `borgmatic` deal with it.

So this is the plist file I ended up with.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Unique identifier for this job -->
    <key>Label</key>
    <string>pkuehn.borgmatic</string>
    
    <!-- The command to run -->
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/borgmatic</string>
    </array>
    
    <!-- Run every 10 min (600 seconds) -->
    <key>StartInterval</key>
    <integer>600</integer>
    
    <!-- Working directory -->
    <key>WorkingDirectory</key>
    <string>/Users/pkuehn</string>
    
    <!-- Environment variables -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>/Users/pkuehn</string>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/pkuehn/Library/Logs/borgmatic-std.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/pkuehn/Library/Logs/borgmatic-err.log</string>
    
    <!-- Don't run at load time, only on schedule -->
    <key>RunAtLoad</key>
    <false/>
    
    <!-- Don't keep the job alive continuously -->
    <key>KeepAlive</key>
    <false/>
    
    <!-- Process type for better resource management -->
    <key>ProcessType</key>
    <string>Background</string>
    
    <!-- Throttle interval to prevent rapid respawning -->
    <key>ThrottleInterval</key>
    <integer>30</integer>
    
    <!-- Resource limits for backup process -->
    <key>SoftResourceLimits</key>
    <dict>
        <key>CPU</key>
        <integer>3600</integer> <!-- 30 minutes max CPU time -->
        <key>NumberOfFiles</key>
        <integer>1024</integer>
    </dict>
</dict>
</plist>
```

But after placing the service in `~/Library/LaunchAgents/pkuehn.borgmatic.plist`, I was greeted with this nice pop-up:

> Python requires Full Disk Access <!-- TODO: check the popup again; add link to FDA documentation -->

Which I of course denied.
I do not want my global Python interpreter to have full disk access, but just `borgmatic`, which is written in Python.
So, I required a wrapper app to deal with the FDA's permission. <!-- TO-DO: look for the blog post that solved this problem -->
The solution of this blog post's author was to write a wrapper for `borgmatic`, which is not written in an interpreted language (here, GoLang), to limit the permission to just this one wrapper-binary.
I also went for the simplest possible solution and wrote a Go wrapper.
It checks the path of `borgmatic`, runs the binary, and forwards the I/O to the OS's I/O.

```go
package main

import (
	"log"
	"os"
	"os/exec"
)

func main () {
    fname, err := exec.LookPath("borgmatic")
	if err != nil {
        log.Fatal(err)
    }
    cmd := exec.Command(fname)
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    if err := cmd.Run(); err != nil {
        log.Fatal(err)
    }
}
```

After a short `go build` and `cp'ing the binary to the PATH, I corrected the path in the previous plist file to 

```xml
<!-- The command to run -->
<key>ProgramArguments</key>
<array>
    <string>/Users/pkuehn/bin/borgmatic-wrapper</string>
</array>
```

And that's it.
After loading and starting the service, I was greeted with the FDA pop-up again -- but now for my wrapper app, and my backups are running regularly 💪

```sh
storagebox: Listing archives
macbook-2025-08-25T21:30:47.116654   Mon, 2025-08-25 21:30:47 [a51ffcc5f88e0fe68f9e2092558e08d622faaef6b6984b88a755d587875abf42]
macbook-2025-08-26T17:05:31.543293   Tue, 2025-08-26 17:05:32 [287f7aae1d9e342233677d01b49ed940eac143423867079e5111b0aca3eebe8a]
macbook-2025-08-27T22:14:35.876593   Wed, 2025-08-27 22:14:36 [36e49f6dc52e520b466527200703583231484a8d1825833819a5ece1a19954d8]
... 21 more snapshots
macbook-2025-09-10T16:59:04.454872   Wed, 2025-09-10 16:59:05 [693445c4040ddf59b0b89ad09e433481798aaad3107a5bcf4b0d2af3c6f9f317]
macbook-2025-09-10T17:32:57.683485   Wed, 2025-09-10 17:32:58 [1e2460041c7894f91b7797e2121ccf53bc4341dc39756f274490684844fb81b0]
macbook-2025-09-11T09:40:37.482414   Thu, 2025-09-11 09:40:38 [1432754d70f288e82b76317a0df478978b3c25695253abe3a095bfde4f97840d]
storagebox-helsinki: Listing archives
macbook-2025-09-04T15:48:58.497271   Thu, 2025-09-04 15:48:59 [6f6204352938aa8c86f6d7ed261c96b2520b60587ab6d2f5f516f57143199437]
macbook-2025-09-04T16:40:59.401094   Thu, 2025-09-04 16:41:00 [17d882dbcaecb0ca388039993c3696aaeee8d2ab9c6552bf49af750e597eb92a]
macbook-2025-09-05T15:51:06.984910   Fri, 2025-09-05 15:51:08 [385244415e2ba7e175b302dc424de9600254e82e45b4ab8f5f79ba878ce13bb1]
... 12 more snapshots
macbook-2025-09-10T14:44:02.471958   Wed, 2025-09-10 14:44:03 [a49ea4c49f2605d508efafc7e864ddb5a75736b6f37f05eb0b095f4c07553fed]
macbook-2025-09-10T17:02:22.104919   Wed, 2025-09-10 17:02:23 [a7734cd44fde108b594a048debc09b492efaa93c2947858f80727c194d637059]
macbook-2025-09-11T09:44:01.122305   Thu, 2025-09-11 09:44:02 [ea2bba31169e8db51288219ed0c0931f9d4fc09837668268793c221494420100]
```

## Summary

1. Set up `borgmatic` to your liking and with different repositories to adhere to the 3-2-1 rule
2. Compile a wrapper app for borgmatic to correctly set the Full Disk Access permissions to just the wrapper instead of Python.
3. Write your `.plist` file and place it in `$HOME/Library/LaunchAgents`. You find documentation references and my file as an example above.
4. Load and launch your service file and enjoy your automated background service for borgmatic.


[^1]: The last time was in 2019, when I lost some photos after I switched from Linux to (ironically) MacOS for half a year and forgot to back up my photos, before wiping the system as a whole.
[^2]: WTF Apple ?!?!?!??!!!??


