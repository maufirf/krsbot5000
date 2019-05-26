# krsbot5000
A Discord bot that shitposts about Student Study Plan
---------------------

**krsbot5000** (_or in the proper way of naming, KRSbot5000_) is a bot that posts a
randomly-generated academic study plan cards that is found in most of the university,
or at least the author's country's universities. It's basically a shitpost bot.

The bot is still in the development state and only available in Discord, and limited
to a few discord servers for beta testing and debugging. The final form of the bot
will be deployed as Facebook Page bot that runs the page under the same name.

The only direct user interaction expected to the bots are:
1. In Discord, users can generate study plan cards at their own will using commands
2. In Facebook and web interface, users can add more data (like university or courses)

There are might some additions in the future.

## `courses.json`
`courses.json` is the database file the bot gets its data. You can help me adding more
data in current format (the UPPERCASE text is the string you can edit. Take note that
you should replace it with your own **lowercase** string except for aliases.):
```json
{
    "undergrad": {
        "UNIVERSITY_CODENAME_1": {
            "aliases": [
                "ALIAS 1",
                "ALIAS 2",
                ...
                "ALIAS N"
            ],
            "faculties": {
                "FACULTY_CODENAME": {
                    "aliases:": [...],
                    "majors": {
                        "MAJOR_CODENAME_1": {
                            "aliases": [...],
                            "courses": [
                                ["COURSE_NAME_1", CREDIT, ["TAG 1", "TAG 2", ..., "TAG N"]]
                                ["COURSE_NAME_2", ...]
                                ...
                            ]
                        },
                        "MAJOR_CODENAME_2": {...}
                        ...
                    }
                },
                "FACULTY_CODENAME_2": {...}
                ...
            }
        },
        "UNIVERSITY_CODENAME_2": {...}
        ...
    },
    "postgrad": {
        ...
    },
    "doctoral": {
        ...
    },
    "misc": {
        ...
    }
}
```

Example:
```json
{
    "undergrad": {
        "unj": {
            "aliases": [
                "Universitas Negeri Jakarta",
                "Kampus Pergerakan",
                "Kampus Hijau"
            ],
            "faculties": {
                "fmipa": {
                    "aliases:": ["Fakultas Matematika dan Ilmu Pengetahuan Alam"],
                    "majors": {
                        "ilkom": {
                            "aliases": ["Ilmu Komputer"],
                            "courses": [
                                ["Operating System", 3, ["operating system", "computer architecture", "computer science"]]
                                ["Computer System Organization", 3, ["microcontroller", "embedded system"]]
                            ]
                        }
                    }
                }
            }
        }
    }
}
```

You can send the JSON file to [parampaa2@gmail.com](mailto:parampaa2@gmail.com) and put
"JSON Submission for KRSbot5000" in the subject. Or alternatively, you can just make
a pull request to make another JSON file with different name (for example, `US_courses.json`)
and put it under the folder called `user_courses` (please make it if there is still none.)

If you are willing to wait, i am still making the web interface to submit such things
that is obviously user-friendly without the JSON hassle thing.

## Big Thanks
Thanks to all of the **Bot Appreciation Society** members for the support and the
inspiration to make some hilarious shitpost bots. Love y'all.