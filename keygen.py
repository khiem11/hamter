import base64

exec(base64.b64decode('aW1wb3J0IGFzeW5jaW8KaW1wb3J0IGFpb2h0dHAKaW1wb3J0IHRpbWUKaW1wb3J0IHJhbmRvbQppbXBvcnQgc3RyaW5nCmZyb20gY29sb3JhbWEgaW1wb3J0IGluaXQsIEZvcmUKZnJvbSBmYWtlX3VzZXJhZ2VudCBpbXBvcnQgVXNlckFnZW50CmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lCgphcHBfdG9rZW5fYmlrZSA9ICdkMjg3MjFiZS1mZDJkLTRiNDUtODY5ZS05ZjI1M2I1NTRlNTAnCnByb21vX2lkX2Jpa2UgPSAnNDNlMzU5MTAtYzE2OC00NjM0LWFkNGYtNTJmZDc2NGE4NDNmJwphcHBfdG9rZW5fY2xvbmUgPSAnNzRlZTBiNWItNzc1ZS00YmVlLTk3NGYtNjNlN2Y0ZDViYWNiJwpwcm9tb19pZF9jbG9uZSA9ICdmZTY5M2IyNi1iMzQyLTQxNTktODgwOC0xNWUzZmY3Zjg3NjcnCmFwcF90b2tlbl9jdWJlID0gJ2QxNjkwYTA3LTM3ODAtNDA2OC04MTBmLTliNWJiZjI5MzFiMicKcHJvbW9faWRfY3ViZSA9ICdiNDE3MDg2OC1jZWYwLTQyNGYtOGViOS1iZTA2MjJlOGU4ZTMnCmFwcF90b2tlbl90cmFpbiA9ICc4MjY0N2Y0My0zZjg3LTQwMmQtODhkZC0wOWE5MDAyNTMxM2YnCnByb21vX2lkX3RyYWluID0gJ2M0NDgwYWM3LWUxNzgtNDk3My04MDYxLTllZDViMmUxNzk1NCcKCnBlcmNvYmFhbiA9IDIwCm51bmdndSA9IDIwCm91dHB1dF9maWxlID0gInZvdWNoZXIudHh0Igppbml0KGF1dG9yZXNldD1UcnVlKQp1YSA9IFVzZXJBZ2VudCgpCgpkZWYgZ2VuZXJhdGVfY2xpZW50X2lkKCk6CiAgICB0aW1lc3RhbXAgPSBzdHIoaW50KHRpbWUudGltZSgpICogMTAwMCkpCiAgICByYW5kb21fZGlnaXRzID0gJycuam9pbihyYW5kb20uY2hvaWNlcyhzdHJpbmcuZGlnaXRzLCBrPTE5KSkKICAgIHJldHVybiBmInt0aW1lc3RhbXB9LXtyYW5kb21fZGlnaXRzfSIKCmRlZiBnZW5lcmF0ZV9ldmVudF9pZCgpOgogICAgcGFydHMgPSBbCiAgICAgICAgJycuam9pbihyYW5kb20uY2hvaWNlcyhzdHJpbmcuYXNjaWlfbG93ZXJjYXNlICsgc3RyaW5nLmRpZ2l0cywgaz04KSksCiAgICAgICAgJycuam9pbihyYW5kb20uY2hvaWNlcyhzdHJpbmcuZGlnaXRzLCBrPTQpKSwKICAgICAgICAnJy5qb2luKHJhbmRvbS5jaG9pY2VzKHN0cmluZy5hc2NpaV9sb3dlcmNhc2UgKyBzdHJpbmcuZGlnaXRzLCBrPTQpKSwKICAgICAgICAnJy5qb2luKHJhbmRvbS5jaG9pY2VzKHN0cmluZy5hc2NpaV9sb3dlcmNhc2UgKyBzdHJpbmcuZGlnaXRzLCBrPTQpKSwKICAgICAgICAnJy5qb2luKHJhbmRvbS5jaG9pY2VzKHN0cmluZy5hc2NpaV9sb3dlcmNhc2UgKyBzdHJpbmcuZGlnaXRzLCBrPTEyKSkKICAgIF0KICAgIHJldHVybiAnLScuam9pbihwYXJ0cykKCmFzeW5jIGRlZiBnZXRfcHJvbW9fY29kZShhcHBfdG9rZW46IHN0ciwgcHJvbW9faWQ6IHN0ciwga2V5X3R5cGU6IHN0cik6CiAgICBoZWFkZXJzID0geyJDb250ZW50LVR5cGUiOiAiYXBwbGljYXRpb24vanNvbjsgY2hhcnNldD11dGYtOCIsICJIb3N0IjogImFwaS5nYW1lcHJvbW8uaW8iLCAiVXNlci1BZ2VudCI6IHVhLnJhbmRvbX0KICAgIGFzeW5jIHdpdGggYWlvaHR0cC5DbGllbnRTZXNzaW9uKGhlYWRlcnM9aGVhZGVycykgYXMgaHR0cF9jbGllbnQ6CiAgICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgY2xpZW50X2lkID0gZ2VuZXJhdGVfY2xpZW50X2lkKCkKICAgICAgICAgICAganNvbl9kYXRhID0geyJhcHBUb2tlbiI6IGFwcF90b2tlbiwgImNsaWVudElkIjogY2xpZW50X2lkLCAiY2xpZW50T3JpZ2luIjogImRldmljZWlkIn0KICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgcmVzcG9uc2UgPSBhd2FpdCBodHRwX2NsaWVudC5wb3N0KHVybD0iaHR0cHM6Ly9hcGkuZ2FtZXByb21vLmlvL3Byb21vL2xvZ2luLWNsaWVudCIsIGpzb249anNvbl9kYXRhKQogICAgICAgICAgICAgICAgcmVzcG9uc2VfanNvbiA9IGF3YWl0IHJlc3BvbnNlLmpzb24oKQogICAgICAgICAgICAgICAgYWNjZXNzX3Rva2VuID0gcmVzcG9uc2VfanNvbi5nZXQoImNsaWVudFRva2VuIikKICAgICAgICAgICAgICAgIGlmIG5vdCBhY2Nlc3NfdG9rZW46CiAgICAgICAgICAgICAgICAgICAgcHJpbnQoRm9yZS5MSUdIVFJFRF9FWCArIGYiXHJbe2tleV90eXBlfV0gVHJ5aW5nIHRvIGdldCB0b2tlbiBhZ2Fpbi4uIiwgZW5kPSIiLCBmbHVzaD1UcnVlKQogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgIGh0dHBfY2xpZW50LmhlYWRlcnNbIkF1dGhvcml6YXRpb24iXSA9IGYiQmVhcmVyIHthY2Nlc3NfdG9rZW59IgogICAgICAgICAgICAgICAgYXdhaXQgYXN5bmNpby5zbGVlcCgxKQogICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICBmb3IgXyBpbiByYW5nZShwZXJjb2JhYW4pOgogICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgZXZlbnRfaWQgPSBnZW5lcmF0ZV9ldmVudF9pZCgpCiAgICAgICAgICAgICAgICAgICAgICAgIGpzb25fZGF0YSA9IHsicHJvbW9JZCI6IHByb21vX2lkLCAiZXZlbnRJZCI6IGV2ZW50X2lkLCAiZXZlbnRPcmlnaW4iOiAidW5kZWZpbmVkIn0KICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2UgPSBhd2FpdCBodHRwX2NsaWVudC5wb3N0KHVybD0iaHR0cHM6Ly9hcGkuZ2FtZXByb21vLmlvL3Byb21vL3JlZ2lzdGVyLWV2ZW50IiwganNvbj1qc29uX2RhdGEpCiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlX2pzb24gPSBhd2FpdCByZXNwb25zZS5qc29uKCkKICAgICAgICAgICAgICAgICAgICAgICAgaWYgcmVzcG9uc2VfanNvbi5nZXQoImhhc0NvZGUiLCBGYWxzZSk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBqc29uX2RhdGEgPSB7InByb21vSWQiOiBwcm9tb19pZH0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlID0gYXdhaXQgaHR0cF9jbGllbnQucG9zdCh1cmw9Imh0dHBzOi8vYXBpLmdhbWVwcm9tby5pby9wcm9tby9jcmVhdGUtY29kZSIsIGpzb249anNvbl9kYXRhKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2VfanNvbiA9IGF3YWl0IHJlc3BvbnNlLmpzb24oKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgcHJvbW9fY29kZSA9IHJlc3BvbnNlX2pzb24uZ2V0KCJwcm9tb0NvZGUiKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgcHJvbW9fY29kZToKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBub3cgPSBkYXRldGltZS5ub3coKS5zdHJmdGltZSgiJWQvJW0gJUg6JU06JVMiKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHByaW50KEZvcmUuTElHSFRHUkVFTl9FWCArIGYiXHJbIHtub3d9IF0ge2tleV90eXBlfSBWb3VjaGVyOiB7cHJvbW9fY29kZX0gICIsIGZsdXNoPVRydWUpCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgd2l0aCBvcGVuKG91dHB1dF9maWxlLCAnYScpIGFzIGY6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYud3JpdGUoZiJ7cHJvbW9fY29kZX1cbiIpCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGVycm9yOgogICAgICAgICAgICAgICAgICAgICAgICBwcmludChGb3JlLkxJR0hUUkVEX0VYICsgZiJcclt7a2V5X3R5cGV9XSBFcnJvcjoge2Vycm9yfSIsIGZsdXNoPVRydWUpCiAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgYXdhaXQgYXN5bmNpby5zbGVlcChudW5nZ3UpCiAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgIGFjYWsgPSByYW5kb20ucmFuZGludCgxLCA1KQogICAgICAgICAgICAgICAgcHJpbnQoZiJcclt7a2V5X3R5cGV9XSBSYW5kb20gZGVsYXk6IHthY2FrfSBzZWNvbmRzICAgICAgICAgICAiLCBlbmQ9IiIsIGZsdXNoPVRydWUpCiAgICAgICAgICAgICAgICBhd2FpdCBhc3luY2lvLnNsZWVwKGFjYWspCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIHByaW50KGYiR+G6t3AgbOG7l2k6IHtlfSIpCiAgICAgICAgICAgICAgICBwcmludCgixJDhu6NpIDMwMCBnacOieSB0csaw4bubYyBraGkgdGjhu60gbOG6oWkuLi4iKQogICAgICAgICAgICAgICAgYXdhaXQgYXN5bmNpby5zbGVlcCgzMDApCiAgICAgICAgICAgICAgICBwcmludCgiVGnhur9wIHThu6VjIGNo4bqheS4uLiIpCgphc3luYyBkZWYgbWFpbigpOgogICAgd2hpbGUgVHJ1ZToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHByaW50KEZvcmUuTElHSFRCTFVFX0VYICsgIlxyS0VZR0VOIEhBTVNURVIgS09NQkFUIikKICAgICAgICAgICAgcHJpbnQoRm9yZS5MSUdIVENZQU5fRVggKyBmIlxyIEpvaW4gUEsgQWlyZHJvcCDEkeG7gyBuaOG6rW4gY8OhYyB0b29sIEZSRUUgaGnhu4d1IGNo4buJbmggY+G7sWMgeOG7i24gbmjDqSA6IGh0dHBzOi8vdC5tZS9wa2FpcmRyb3A5OSAgICAgICBcbiIsIGVuZD0iIiwgZmx1c2g9VHJ1ZSkKICAgICAgICAgICAgcHJpbnQoRm9yZS5SRUQgKyAiIFRPT0wgTsOAWSBMw4AgRlJFRSwgTuG6vlUgQuG6oE4gUEjhuqJJIFRS4bqiICQgxJDhu4IgQ8OTIE7DkyBMw4AgQuG6oE4gxJDDgyBC4buKIEzhu6pBICEiICkKICAgICAgICAgICAgcHJpbnQoRm9yZS5ZRUxMT1cgKyAixJBhbmcgR2VuIEtleSwgdnVpIGzDsm5nIGNo4budIC4uLiAiKQogICAgICAgICAgICAKICAgICAgICAgICAgdGFza3MgPSBbCiAgICAgICAgICAgICAgICBhc3luY2lvLmNyZWF0ZV90YXNrKGdldF9wcm9tb19jb2RlKGFwcF90b2tlbl9iaWtlLCBwcm9tb19pZF9iaWtlLCAiQklLRSIpKSwKICAgICAgICAgICAgICAgIGFzeW5jaW8uY3JlYXRlX3Rhc2soZ2V0X3Byb21vX2NvZGUoYXBwX3Rva2VuX2N1YmUsIHByb21vX2lkX2N1YmUsICJDVUJFIikpLAogICAgICAgICAgICAgICAgYXN5bmNpby5jcmVhdGVfdGFzayhnZXRfcHJvbW9fY29kZShhcHBfdG9rZW5fdHJhaW4sIHByb21vX2lkX3RyYWluLCAiVFJBSU4iKSksCiAgICAgICAgICAgICAgICBhc3luY2lvLmNyZWF0ZV90YXNrKGdldF9wcm9tb19jb2RlKGFwcF90b2tlbl9jbG9uZSwgcHJvbW9faWRfY2xvbmUsICJDTE9ORSIpKQogICAgICAgICAgICBdCiAgICAgICAgICAgIAogICAgICAgICAgICBhd2FpdCBhc3luY2lvLmdhdGhlcigqdGFza3MpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICBwcmludChmIkfhurdwIGzhu5dpOiB7ZX0iKQogICAgICAgICAgICBwcmludCgixJDhu6NpIDMwMCBnacOieSB0csaw4bubYyBraGkgdGjhu60gbOG6oWkuLi4iKQogICAgICAgICAgICBhd2FpdCBhc3luY2lvLnNsZWVwKDMwMCkKICAgICAgICAgICAgcHJpbnQoIlRp4bq/cCB04bulYyBjaOG6oXkuLi4iKQoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIGFzeW5jaW8ucnVuKG1haW4oKSkK').decode())