import json
from collections import OrderedDict
from datetime import datetime

# ── Recommendations ────────────────────────────────────────────────────────

RECS = {
    'PP1149739': "Sorkin (DealBook founder, Squawk Box) + Weisenthal (Bloomberg Odd Lots). Actual thesis comparing the current AI/speculation bubble to 1929 patterns. Not vibes — Sorkin wrote a book on this.",
    'PP1149051': "Cloudflare handles ~20% of internet traffic. Prince has unique data on how AI is structurally breaking the search-driven web economy. Specific and consequential.",
    'PP1162234': "Center for Humane Technology + Future of Life Institute. Promises specific mechanisms, not hand-waving. Two people who've been doing this work for years.",
    'PP1150099': "Schiller almost never speaks publicly outside Apple events. He was in the room for iPod, iPhone, iPad decisions. Primary source, rare appearance.",
    'PP1150887': "Bolt.new went $0→$40M ARR in 5 months on Claude. Builders with real production data, not consultants speculating. Promises candid takes on AI hype, scaling laws, technical debt.",
    'PP1162516': "Chief Scientist at Sony AI, leading RL researcher at UT Austin. Technical and specific — RL is behind the most impressive breakthroughs but gets less hype than generative AI.",
    'PP1162407': "Cuban is unscripted and says what he thinks. Concrete topic (media business models collapsing under AI), not corporate messaging.",
    'PP1150100': "Rivian CEO + former NASA/Apple engineer. Interactive demo of autonomous robotics. Actual hardware, actual engineering.",
    'PP1162997': "Always sharp, no corporate deference. Live podcast is consistently good.",
    'PP1148557': "Founders of Apptronik and Agility Robotics (makers of Digit) + Sony AI. People actually building and deploying humanoids, not commentating.",
    'PP1148484': "More rigorous than most futurists, data-driven. SXSW institution.",
    'PP1163013': "Lessig is foundational on internet law. AI training data vs open knowledge.",
    'PP1148996': "First-person whistleblower story from inside Meta. Ex-WhatsApp security lead.",
    'PP1149203': "Spotify is one of the most aggressive AI deployers. Operator, not commentator.",
    'PP1150458': "Genuine product thinker actually shipping interesting consumer hardware.",
    'PP1150687': "Live fine-tuning of an open-source model on stage. It either works or it doesn't.",
    'PP1162292': "AI for emergency response where failure = life or death. Honest framing around automation bias. Motorola Solutions + Anthropic.",
    'PP1148565': "Unpublished cognitive neuroscience data on whether AI augmentation is actually just cognitive offloading.",
    # Innovation picks
    'PP1148559': "2018 Nobel laureate who invented checkpoint immunotherapy. Features a 21-year stage IV cancer survivor. You rarely get to hear a Nobel laureate discuss what's next in their field.",
    'PP1162485': "One of the most important consciousness researchers alive — worked with Francis Crick for 16 years. Not a wellness guru; a serious neuroscientist integrating psychedelic phenomenology into empirical research.",
    'PP1162468': "Marine biologist and Nat Geo Explorer running a legit ML project decoding sperm whale communication. Real science, real data.",
    'PP1149095': "Co-founded Center for Humane Technology and Earth Species Project (AI for decoding animal communication). Pairs nicely with the whale talk.",
    'PP1162381': "Two senior DeepMind researchers + a CU Boulder professor who studies digital death. AI simulations of dead people — genuinely novel topic with real depth.",
    'PP1148523': "Samir Patel (Editor in Chief, Quanta Magazine) + Latif Nasser (Radiolab co-host). People who actually do excellent science communication, not content creators.",
    'PP1162254': "A plasma physicist, a founder who actually built a fusion neutron company (SHINE Technologies), and Jacob Goldstein (ex-Planet Money). Honest framing — speakers who will actually disagree.",
    'PP1162938': "Live demo of a person with permanent voice loss using their AI-restored voice on stage. ElevenLabs co-founder. Concrete, not abstract.",
    'PP1148536': "Annual fixture, consistently delivers real analysis. This year: designing for AI agents rather than humans (UX → Agentic Experience). Maeda has the credentials (MIT Media Lab, RISD president, now Microsoft VP).",
    'PP1162227': "Komor's base-editing method was recently used to create a custom therapy for an infant with a deadly rare disease. Researchers whose work is literally saving children's lives.",
    'PP1162439': "Eva Galperin (EFF) is one of the most respected cybersecurity/digital rights people alive. Organized by Human Rights Foundation.",
    'PP1162462': "Jimmy Wales + the former Google News ecosystem director. Existential question, people with direct experience.",
    'PP1162583': "World-class consciousness researcher (15M+ view TED talk, bestselling author). Art meets neuroscience.",
    'PP1149920': "If you care about startups, the head of YC during the AI wave is worth hearing.",
    'PP1149793': "Mayors of Chattanooga and Phoenix dealing with real data center infrastructure consequences. Not consultants theorizing.",
    'PP1162879': "FDA/CDC/NIH workforce cuts + AI triage. Timely and specific.",
    'PP1163019': "Overexposed but both are legitimate researchers. Making a special announcement.",
    'PP1162595': "Actual open-source brain-computer interface hardware builder, live demo on stage.",
    'PP1162389': "Grows brain organoids from stem cells, sent them to the ISS. Published research comparing Neanderthal and modern human brain development.",
}

# ── Load data ──────────────────────────────────────────────────────────────

with open('/tmp/sxsw_tech_ai_speakers_events.json') as f:
    tech_ai_data = json.load(f)

with open('/tmp/sxsw_innovation_events.json') as f:
    innovation_raw = json.load(f)

# ── Helpers ────────────────────────────────────────────────────────────────

DAY_LABELS = {
    '2026-03-12': 'Thursday, March 12',
    '2026-03-13': 'Friday, March 13',
    '2026-03-14': 'Saturday, March 14',
    '2026-03-15': 'Sunday, March 15',
    '2026-03-16': 'Monday, March 16',
    '2026-03-17': 'Tuesday, March 17',
    '2026-03-18': 'Wednesday, March 18',
}

FORMAT_COLORS = {
    'Panel': ['#dbeafe', '#1e40af'],
    'Fireside Chat': ['#fce7f3', '#9d174d'],
    'Workshop': ['#d1fae5', '#065f46'],
    'Presentation': ['#e0e7ff', '#3730a3'],
    'Podcast': ['#fef3c7', '#92400e'],
    'Featured Session': ['#fee2e2', '#991b1b'],
    'Keynote': ['#fecaca', '#7f1d1d'],
    'Solo': ['#f3e8ff', '#6b21a8'],
    'Conversation': ['#ccfbf1', '#134e4a'],
    'Core Conversation': ['#cffafe', '#155e75'],
    'Meet Up': ['#fde68a', '#78350f'],
    'Mentor Session': ['#e2e8f0', '#334155'],
    'Book Reading': ['#fbcfe8', '#831843'],
    'Book Signing': ['#fecdd3', '#9f1239'],
    'XR Experience': ['#c7d2fe', '#4338ca'],
    'Pitch Event': ['#bfdbfe', '#1e3a8a'],
    'Film Screening': ['#fde68a', '#713f12'],
    'Exhibition': ['#d9f99d', '#365314'],
    'Activation': ['#a7f3d0', '#064e3b'],
    'Special Event': ['#fed7aa', '#7c2d12'],
    'Comedy': ['#fca5a5', '#991b1b'],
    'Simulcast': ['#cbd5e1', '#475569'],
    'Registration': ['#e2e8f0', '#64748b'],
    'Party': ['#f0abfc', '#86198f'],
    'Bookstore': ['#fecdd3', '#881337'],
}

def esc(s):
    return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def format_time(iso):
    if not iso: return ''
    d = datetime.fromisoformat(iso)
    return d.strftime('%-I:%M %p').lower()

def time_range(start, end):
    s = format_time(start)
    e = format_time(end)
    if not s: return ''
    return f'{s} – {e}' if e else s


# ── Build Tech & AI events ────────────────────────────────────────────────

tech_events = {}
for r in tech_ai_data:
    for e in r['events']:
        eid = e['event_id']
        if eid not in tech_events:
            tech_events[eid] = {**e, 'speakers': []}
        tech_events[eid]['speakers'].append({
            'name': r['name'],
            'title': r['title'],
            'company': r['company'],
            'speaker_url': r['speaker_url'],
        })

tech_sorted = sorted(tech_events.values(), key=lambda e: e.get('start_time') or 'zzzz')
tech_speakers = sorted(tech_ai_data, key=lambda r: r['name'].lower())

# ── Build Innovation events ───────────────────────────────────────────────

innov_events = []
innov_speakers_map = {}
for e in innovation_raw:
    evt = {
        'event_id': e.get('event_id', ''),
        'name': e.get('name', ''),
        'format': e.get('format') or e.get('category') or '',
        'track': e.get('track', ''),
        'date': e.get('date', ''),
        'start_time': e.get('start_time', ''),
        'end_time': e.get('end_time', ''),
        'venue': '',
        'event_url': f"https://schedule.sxsw.com/2026/events/{e.get('event_id', '')}",
        'description': e.get('description') or '',
        'speakers': [],
    }
    v = e.get('venue') or {}
    parent = v.get('parent_venue_name') or ''
    room = v.get('name') or ''
    evt['venue'] = f"{parent} - {room}" if parent and room else parent or room

    for c in (e.get('contributors') or []):
        spk = {
            'name': c.get('name', ''),
            'title': c.get('title', ''),
            'company': c.get('company', ''),
            'speaker_url': f"https://schedule.sxsw.com/2026/contributors/{c.get('entity_id', '')}",
        }
        evt['speakers'].append(spk)
        sid = c.get('entity_id')
        if sid and sid not in innov_speakers_map:
            innov_speakers_map[sid] = spk

    innov_events.append(evt)

innov_sorted = sorted(innov_events, key=lambda e: e.get('start_time') or 'zzzz')
innov_speakers = sorted(innov_speakers_map.values(), key=lambda s: s['name'].lower())


# ── HTML generators ───────────────────────────────────────────────────────

def group_by_date(events):
    groups = OrderedDict()
    for e in events:
        d = e['date'] or 'TBD'
        if d not in groups:
            groups[d] = []
        groups[d].append(e)
    return groups

def build_events_html(sorted_events, prefix):
    html = ''
    groups = group_by_date(sorted_events)
    for date, evts in groups.items():
        label = DAY_LABELS.get(date, date)
        html += f'<h2 class="day-heading" id="{prefix}-d-{date}">{label}</h2>\n'
        for e in evts:
            tr = time_range(e.get('start_time'), e.get('end_time'))
            desc = esc(e.get('description', ''))
            venue = esc(e.get('venue', ''))
            fmt = esc(e.get('format', ''))
            eid = esc(e.get('event_id', ''))
            bg, fg = FORMAT_COLORS.get(e.get('format', ''), ['#f0f0f0', '#777'])
            start_iso = esc(e.get('start_time', ''))
            end_iso = esc(e.get('end_time', ''))
            raw_desc = (e.get('description', '') or '').replace('"', '&quot;')
            event_name_attr = esc(e.get('name', ''))
            event_url_attr = esc(e.get('event_url', ''))

            speakers_html = ', '.join(
                f'<a class="speaker" href="{s["speaker_url"]}" target="_blank">{esc(s["name"])}</a>'
                for s in e.get('speakers', [])
            )

            desc_html = ''
            if desc:
                desc_html = f'<details><summary class="more">details</summary><p class="desc">{desc}</p></details>'

            cal_html = ''
            if start_iso and end_iso:
                cal_html = '<div class="cal-links"><a class="cal-link" href="#" onclick="addToGcal(this.closest(\'.ev\'));return false">+ gcal</a><a class="cal-link" href="#" onclick="addToIcal(this.closest(\'.ev\'));return false">+ ical</a></div>'

            track_tag = ''
            track_val = esc(e.get('track', ''))
            if track_val:
                track_tag = f'<span class="track-tag">{track_val}</span>'

            raw_eid = e.get('event_id', '')
            rec_note = RECS.get(raw_eid, '')
            rec_attr = ' data-rec="1"' if rec_note else ''
            rec_html = ''
            if rec_note:
                rec_html = f'<div class="rec"><span class="rec-icon" title="Recommended">&#10024;</span><span class="rec-text">{esc(rec_note)}</span></div>'

            html += f'''<div class="ev" data-fmt="{fmt}" data-eid="{eid}" data-start="{start_iso}" data-end="{end_iso}" data-title="{event_name_attr}" data-venue="{esc(e.get('venue',''))}" data-desc="{raw_desc}" data-url="{event_url_attr}"{rec_attr}>
<div class="ev-top">
<div class="ev-main">
<div class="meta">{f'<span class="time">{tr}</span>' if tr else ''}{f'<span class="fmt" style="background:{bg};color:{fg}">{fmt}</span>' if fmt else ''}{track_tag}</div>
<a class="title" href="{e.get('event_url','')}" target="_blank">{esc(e.get('name',''))}</a>
{f'<div class="venue">{venue}</div>' if venue else ''}
</div>
<button class="fav-btn" data-eid="{eid}" title="Favourite" aria-label="Favourite">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
</button>
</div>
{rec_html}
{desc_html}
{f'<div class="speakers">{speakers_html}</div>' if speakers_html else ''}
{cal_html}
</div>
'''
    return html, groups

def build_speakers_html(speakers):
    html = '<div class="speaker-grid">\n'
    for s in speakers:
        role = ', '.join(filter(None, [s['title'], s['company']]))
        html += f'<a class="sp" href="{s["speaker_url"]}" target="_blank"><span class="sp-name">{esc(s["name"])}</span>'
        if role:
            html += f'<span class="sp-role">{esc(role)}</span>'
        html += '</a>\n'
    html += '</div>'
    return html

def build_day_nav(groups, prefix):
    nav = ''
    for date in groups:
        parts = date.split('-')
        short = DAY_LABELS.get(date, date).split(',')[0][:3] + ' ' + parts[2] if len(parts) == 3 else date
        nav += f'<a class="nav-day" href="#{prefix}-d-{date}">{short}</a>'
    return nav

def build_fmt_checks(events):
    formats = sorted(set(e.get('format') or '' for e in events if e.get('format')))
    html = ''
    for fmt in formats:
        bg, fg = FORMAT_COLORS.get(fmt, ['#f0f0f0', '#777'])
        html += f'<label class="fmt-check" style="--bg:{bg};--fg:{fg}"><input type="checkbox" checked data-fmt="{esc(fmt)}"><span class="fmt-dot"></span>{esc(fmt)}</label>'
    return html


# ── Build sections ────────────────────────────────────────────────────────

tech_events_html, tech_groups = build_events_html(tech_sorted, 'tech')
tech_speakers_html = build_speakers_html(tech_speakers)
tech_nav = build_day_nav(tech_groups, 'tech')
tech_fmt = build_fmt_checks(tech_sorted)

innov_events_html, innov_groups = build_events_html(innov_sorted, 'innov')
innov_speakers_html = build_speakers_html(innov_speakers)
innov_nav = build_day_nav(innov_groups, 'innov')
innov_fmt = build_fmt_checks(innov_sorted)

n_tech_events = len(tech_sorted)
n_tech_speakers = len(tech_speakers)
n_innov_events = len(innov_sorted)
n_innov_speakers = len(innov_speakers)

# ── Final HTML ────────────────────────────────────────────────────────────

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SXSW 2026 Schedule</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #fff; color: #111; line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}}
.wrap {{ max-width: 680px; margin: 0 auto; padding: 0 20px 80px; }}

/* Header */
header {{ padding: 32px 0 16px; }}
header h1 {{ font-size: 22px; font-weight: 700; letter-spacing: -0.03em; color: #000; }}
header p {{ color: #666; font-size: 13px; margin-top: 4px; }}
.search {{
  padding: 10px 14px; width: 100%; border: 1.5px solid #ddd;
  border-radius: 10px; font-size: 14px; outline: none; background: #f8f8f8;
  margin: 10px 0 4px; transition: border-color 0.15s, background 0.15s;
}}
.search:focus {{ border-color: #888; background: #fff; }}
.search::placeholder {{ color: #aaa; }}

/* Top-level track tabs */
.track-tabs {{
  display: flex; gap: 0; border-bottom: 2px solid #eee;
}}
.track-tab {{
  padding: 12px 20px; font-size: 14px; font-weight: 600;
  color: #aaa; cursor: pointer; border: none; background: none;
  border-bottom: 2.5px solid transparent; margin-bottom: -2px;
  transition: color 0.15s;
}}
.track-tab:hover {{ color: #555; }}
.track-tab.active {{ color: #000; border-bottom-color: #000; }}
.track-tab small {{ font-weight: 400; color: inherit; opacity: 0.6; }}
.track-section {{ display: none; }}
.track-section.active {{ display: block; }}

/* Sub tabs */
.tabs {{
  display: flex; gap: 0; border-bottom: 1px solid #eee;
}}
.tab {{
  padding: 11px 18px; font-size: 13px; font-weight: 600;
  color: #aaa; cursor: pointer; border: none; background: none;
  border-bottom: 2px solid transparent; margin-bottom: -1px;
  transition: color 0.15s;
}}
.tab:hover {{ color: #555; }}
.tab.active {{ color: #000; border-bottom-color: #000; }}
.fav-count {{
  font-size: 10px; background: #ef4444; color: #fff; border-radius: 8px;
  padding: 1px 6px; margin-left: 4px; font-weight: 700;
  display: none; vertical-align: 1px;
}}
.fav-count.show {{ display: inline; }}
.view {{ display: none; }}
.view.active {{ display: block; }}

/* Sticky controls */
.controls {{
  position: sticky; top: 0; background: #fff; z-index: 10;
  padding: 10px 0 0; border-bottom: 1px solid #eee;
}}
.day-nav {{
  display: flex; gap: 5px; padding: 4px 0 8px;
  overflow-x: auto; scrollbar-width: none;
}}
.day-nav::-webkit-scrollbar {{ display: none; }}
.nav-day {{
  flex-shrink: 0; padding: 6px 14px; border-radius: 18px;
  font-size: 12px; font-weight: 600; background: #f3f3f3; color: #555;
  text-decoration: none; white-space: nowrap; transition: background 0.15s;
}}
.nav-day:hover {{ background: #e5e5e5; }}

/* Format filters */
.fmt-filters {{
  display: flex; flex-wrap: wrap; gap: 8px; padding: 8px 0 10px;
  align-items: center;
}}
.fmt-toggle {{
  font-size: 11px; font-weight: 600; border: none; cursor: pointer;
  background: none; color: #888; padding: 0; margin-right: 2px;
  white-space: nowrap; text-decoration: underline;
  text-underline-offset: 2px;
}}
.fmt-toggle:hover {{ color: #333; }}
.fmt-check {{
  display: flex; align-items: center; gap: 5px; cursor: pointer;
  font-size: 11px; font-weight: 600; color: var(--fg);
  -webkit-user-select: none; user-select: none; white-space: nowrap;
}}
.fmt-check input {{ display: none; }}
.fmt-dot {{
  width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0;
  border: 2px solid var(--fg); background: transparent;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.1s;
}}
.fmt-check input:checked ~ .fmt-dot {{ background: var(--fg); }}
.fmt-check input:checked ~ .fmt-dot::after {{
  content: ''; display: block; width: 4px; height: 7px;
  border: solid #fff; border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg); margin-top: -1px;
}}
.fmt-check:not(:has(input:checked)) {{ opacity: 0.3; }}

/* ── Events ── */
.day-heading {{
  font-size: 13px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.06em; color: #000; padding: 28px 0 12px;
  border-bottom: 2px solid #111;
}}
.ev {{
  padding: 16px 0; border-bottom: 1px solid #f0f0f0;
}}
.ev.hidden {{ display: none; }}
.ev-top {{ display: flex; align-items: flex-start; gap: 10px; }}
.ev-main {{ flex: 1; min-width: 0; }}

/* Time + format row */
.meta {{
  display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;
}}
.time {{
  font-size: 13px; font-weight: 700; color: #000;
  font-variant-numeric: tabular-nums;
}}
.fmt {{
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em; padding: 3px 8px; border-radius: 4px;
}}
.track-tag {{
  font-size: 10px; font-weight: 600; color: #888;
  padding: 3px 8px; border-radius: 4px; background: #f3f3f3;
}}

/* Title */
.title {{
  font-size: 16px; font-weight: 700; color: #000;
  text-decoration: none; letter-spacing: -0.02em;
  line-height: 1.35;
}}
.title:hover {{ text-decoration: underline; text-underline-offset: 2px; }}

/* Venue */
.venue {{ font-size: 12px; color: #888; margin-top: 3px; }}

/* Description toggle */
details {{ margin: 8px 0 0; }}
.more {{
  font-size: 12px; color: #999; cursor: pointer; list-style: none;
  font-weight: 500;
}}
.more::-webkit-details-marker {{ display: none; }}
.more::before {{ content: '+ '; font-weight: 700; }}
details[open] .more::before {{ content: '− '; }}
.more:hover {{ color: #444; }}
.desc {{
  font-size: 13px; color: #555; margin: 8px 0 0; line-height: 1.65;
}}

/* Speakers */
.speakers {{
  margin-top: 8px; font-size: 13px; line-height: 1.8; color: #777;
}}
.speaker {{
  color: #333; text-decoration: none; font-weight: 600;
}}
.speaker:hover {{ text-decoration: underline; text-underline-offset: 2px; }}

/* Calendar links */
.cal-links {{ display: flex; gap: 12px; margin-top: 8px; }}
.cal-link {{
  font-size: 11px; font-weight: 600; color: #aaa;
  text-decoration: none; cursor: pointer; transition: color 0.15s;
}}
.cal-link:hover {{ color: #333; }}

/* Recommendations */
.rec {{
  display: flex; align-items: flex-start; gap: 8px;
  margin: 8px 0 2px; padding: 8px 12px;
  background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
}}
.rec-icon {{ font-size: 14px; flex-shrink: 0; line-height: 1.5; }}
.rec-text {{ font-size: 12px; color: #78350f; line-height: 1.55; font-weight: 500; }}
.rec-filter {{
  display: flex; align-items: center; gap: 5px; cursor: pointer;
  font-size: 11px; font-weight: 700; color: #92400e;
  -webkit-user-select: none; user-select: none; white-space: nowrap;
  padding: 4px 10px; border-radius: 14px; background: #fffbeb;
  border: 1px solid #fde68a;
}}
.rec-filter input {{ display: none; }}
.rec-filter .rec-dot {{
  width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0;
  border: 2px solid #92400e; background: transparent;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.1s;
}}
.rec-filter input:checked ~ .rec-dot {{ background: #92400e; }}
.rec-filter input:checked ~ .rec-dot::after {{
  content: ''; display: block; width: 4px; height: 7px;
  border: solid #fff; border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg); margin-top: -1px;
}}

/* Favourite button */
.fav-btn {{
  flex-shrink: 0; background: none; border: none; cursor: pointer;
  color: #ddd; padding: 4px; margin-top: 4px; transition: color 0.15s;
}}
.fav-btn:hover {{ color: #f87171; }}
.fav-btn.active {{ color: #ef4444; }}
.fav-btn.active svg {{ fill: #ef4444; }}

.favs-empty {{
  text-align: center; padding: 60px 20px; color: #999; font-size: 14px;
}}

/* Speakers grid */
.speaker-grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1px; background: #e8e8e8; border: 1px solid #e8e8e8; border-radius: 10px;
  overflow: hidden; margin-top: 20px;
}}
.sp {{
  display: flex; flex-direction: column; padding: 12px 16px;
  background: #fff; text-decoration: none; transition: background 0.1s;
}}
.sp:hover {{ background: #f9f9f9; }}
.sp-name {{ font-size: 14px; font-weight: 600; color: #000; }}
.sp-role {{ font-size: 12px; color: #888; margin-top: 2px; }}

.day-heading.hidden {{ display: none; }}

@media (max-width: 500px) {{
  .wrap {{ padding: 0 16px 80px; }}
  header h1 {{ font-size: 20px; }}
  .title {{ font-size: 15px; }}
  .speaker-grid {{ grid-template-columns: 1fr; }}
  .tab {{ padding: 10px 12px; font-size: 12px; }}
  .track-tab {{ padding: 10px 14px; font-size: 13px; }}
  .ev {{ padding: 14px 0; }}
  .day-heading {{ padding: 24px 0 10px; }}
}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>SXSW 2026</h1>
  <p>March 12–18, Austin TX</p>
  <input type="text" class="search" id="search" placeholder="Search events, speakers, companies...">
</header>

<div class="track-tabs">
  <button class="track-tab active" data-track="tech">Tech & AI <small>({n_tech_events})</small></button>
  <button class="track-tab" data-track="innov">Innovation <small>({n_innov_events})</small></button>
</div>

<!-- Tech & AI -->
<div class="track-section active" id="ts-tech">
  <div class="tabs">
    <button class="tab active" data-view="tech-events">Events</button>
    <button class="tab" data-view="tech-favs">Favs <span class="fav-count" data-fc="tech">0</span></button>
    <button class="tab" data-view="tech-speakers">Speakers ({n_tech_speakers})</button>
  </div>
  <div class="view active" id="v-tech-events">
    <div class="controls">
      <div class="day-nav">{tech_nav}</div>
      <div class="fmt-filters" data-section="tech">
        <button class="fmt-toggle" data-section="tech">Deselect all</button>
        <label class="rec-filter"><input type="checkbox" class="rec-toggle" data-section="tech"><span class="rec-dot"></span>&#10024; recommended</label>
        {tech_fmt}
      </div>
    </div>
    <div class="events-list" data-section="tech">{tech_events_html}</div>
  </div>
  <div class="view" id="v-tech-favs">
    <div class="favs-list" data-section="tech"></div>
  </div>
  <div class="view" id="v-tech-speakers">{tech_speakers_html}</div>
</div>

<!-- Innovation -->
<div class="track-section" id="ts-innov">
  <div class="tabs">
    <button class="tab active" data-view="innov-events">Events</button>
    <button class="tab" data-view="innov-favs">Favs <span class="fav-count" data-fc="innov">0</span></button>
    <button class="tab" data-view="innov-speakers">Speakers ({n_innov_speakers})</button>
  </div>
  <div class="view active" id="v-innov-events">
    <div class="controls">
      <div class="day-nav">{innov_nav}</div>
      <div class="fmt-filters" data-section="innov">
        <button class="fmt-toggle" data-section="innov">Deselect all</button>
        <label class="rec-filter"><input type="checkbox" class="rec-toggle" data-section="innov"><span class="rec-dot"></span>&#10024; recommended</label>
        {innov_fmt}
      </div>
    </div>
    <div class="events-list" data-section="innov">{innov_events_html}</div>
  </div>
  <div class="view" id="v-innov-favs">
    <div class="favs-list" data-section="innov"></div>
  </div>
  <div class="view" id="v-innov-speakers">{innov_speakers_html}</div>
</div>
</div>

<script>
// ── State ──
const LS_FAVS = 'sxsw_favs';
const LS_FMTS_PREFIX = 'sxsw_fmts_';
let favs = new Set(JSON.parse(localStorage.getItem(LS_FAVS) || '[]'));

function getHiddenFmts(section) {{
  return new Set(JSON.parse(localStorage.getItem(LS_FMTS_PREFIX + section) || '[]'));
}}
function saveHiddenFmts(section, set) {{
  localStorage.setItem(LS_FMTS_PREFIX + section, JSON.stringify([...set]));
}}
function saveFavs() {{
  localStorage.setItem(LS_FAVS, JSON.stringify([...favs]));
}}

// ── Track tabs ──
document.querySelectorAll('.track-tab').forEach(t => {{
  t.addEventListener('click', () => {{
    document.querySelectorAll('.track-tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.track-section').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('ts-' + t.dataset.track).classList.add('active');
  }});
}});

// ── Sub tabs (per section) ──
document.querySelectorAll('.tabs').forEach(tabBar => {{
  tabBar.querySelectorAll('.tab').forEach(t => {{
    t.addEventListener('click', () => {{
      const section = tabBar.closest('.track-section');
      section.querySelectorAll('.tabs .tab').forEach(x => x.classList.remove('active'));
      section.querySelectorAll('.view').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      document.getElementById('v-' + t.dataset.view).classList.add('active');
      if (t.dataset.view.endsWith('-favs')) renderFavs(t.dataset.view.replace('-favs', ''));
    }});
  }});
}});

// ── Format filters ──
document.querySelectorAll('.fmt-filters').forEach(container => {{
  const section = container.dataset.section;
  const hiddenFmts = getHiddenFmts(section);
  const checks = container.querySelectorAll('.fmt-check input');
  const toggle = container.querySelector('.fmt-toggle');

  checks.forEach(cb => {{
    if (hiddenFmts.has(cb.dataset.fmt)) cb.checked = false;
  }});

  function updateToggle() {{
    const h = getHiddenFmts(section);
    toggle.textContent = h.size === 0 ? 'Deselect all' : 'Select all';
  }}

  toggle.addEventListener('click', () => {{
    const h = getHiddenFmts(section);
    const allChecked = h.size === 0;
    const newSet = new Set();
    checks.forEach(cb => {{
      cb.checked = !allChecked;
      if (allChecked) newSet.add(cb.dataset.fmt);
    }});
    saveHiddenFmts(section, newSet);
    applyFilters(section);
    updateToggle();
  }});

  checks.forEach(cb => {{
    cb.addEventListener('change', () => {{
      const h = getHiddenFmts(section);
      if (cb.checked) h.delete(cb.dataset.fmt); else h.add(cb.dataset.fmt);
      saveHiddenFmts(section, h);
      applyFilters(section);
      updateToggle();
    }});
  }});

  updateToggle();
}});

// Rec filter
document.querySelectorAll('.rec-toggle').forEach(cb => {{
  cb.addEventListener('change', () => {{
    applyFilters(cb.dataset.section);
  }});
}});

function applyFilters(section) {{
  const hiddenFmts = getHiddenFmts(section);
  const list = document.querySelector(`.events-list[data-section="${{section}}"]`);
  if (!list) return;
  const q = searchQuery;
  const recOnly = document.querySelector(`.rec-toggle[data-section="${{section}}"]`)?.checked || false;
  list.querySelectorAll('.ev').forEach(ev => {{
    const fmtHidden = hiddenFmts.has(ev.dataset.fmt);
    let searchHidden = false;
    if (q) {{
      const text = (ev.dataset.title + ' ' + ev.dataset.venue + ' ' + ev.dataset.desc + ' ' + ev.dataset.fmt + ' ' + ev.textContent).toLowerCase();
      searchHidden = !text.includes(q);
    }}
    const recHidden = recOnly && !ev.dataset.rec;
    ev.classList.toggle('hidden', fmtHidden || searchHidden || recHidden);
  }});
  list.querySelectorAll('.day-heading').forEach(h => {{
    let next = h.nextElementSibling;
    let anyVisible = false;
    while (next && !next.classList.contains('day-heading')) {{
      if (next.classList.contains('ev') && !next.classList.contains('hidden')) {{
        anyVisible = true; break;
      }}
      next = next.nextElementSibling;
    }}
    h.classList.toggle('hidden', !anyVisible);
  }});
}}

// ── Search ──
let searchQuery = '';
document.getElementById('search').addEventListener('input', e => {{
  searchQuery = e.target.value.toLowerCase();
  ['tech', 'innov'].forEach(s => applyFilters(s));
  document.querySelectorAll('.speaker-grid .sp').forEach(sp => {{
    sp.style.display = searchQuery && !sp.textContent.toLowerCase().includes(searchQuery) ? 'none' : '';
  }});
}});

// ── Favourites ──
function updateFavBtns() {{
  document.querySelectorAll('.fav-btn').forEach(b => {{
    b.classList.toggle('active', favs.has(b.dataset.eid));
  }});
  ['tech', 'innov'].forEach(section => {{
    const list = document.querySelector(`.events-list[data-section="${{section}}"]`);
    if (!list) return;
    let count = 0;
    list.querySelectorAll('.fav-btn').forEach(b => {{ if (favs.has(b.dataset.eid)) count++; }});
    const badge = document.querySelector(`.fav-count[data-fc="${{section}}"]`);
    if (badge) {{ badge.textContent = count; badge.classList.toggle('show', count > 0); }}
  }});
}}

document.addEventListener('click', e => {{
  const btn = e.target.closest('.fav-btn');
  if (!btn) return;
  const eid = btn.dataset.eid;
  if (favs.has(eid)) favs.delete(eid); else favs.add(eid);
  saveFavs();
  updateFavBtns();
}});

function renderFavs(section) {{
  const container = document.querySelector(`.favs-list[data-section="${{section}}"]`);
  if (!container) return;
  if (favs.size === 0) {{
    container.innerHTML = '<div class="favs-empty">No favourites yet.<br>Tap the heart on any event to save it.</div>';
    return;
  }}
  let html = '';
  let currentDay = '';
  const evList = document.querySelector(`.events-list[data-section="${{section}}"]`);
  evList.querySelectorAll('.day-heading, .ev').forEach(el => {{
    if (el.classList.contains('day-heading')) {{
      currentDay = el.outerHTML;
    }} else if (favs.has(el.dataset.eid)) {{
      if (currentDay) {{ html += currentDay; currentDay = ''; }}
      html += el.outerHTML;
    }}
  }});
  container.innerHTML = html || '<div class="favs-empty">No favourites in this track.</div>';
}}

// ── Calendar ──
function toGcalDate(iso) {{
  const d = new Date(iso);
  return d.toISOString().replace(/[-:]|\\.\\d{{3}}/g, '');
}}
function addToGcal(ev) {{
  const title = ev.dataset.title;
  const start = toGcalDate(ev.dataset.start);
  const end = toGcalDate(ev.dataset.end);
  const desc = (ev.dataset.desc || '') + '\\n\\n' + (ev.dataset.url || '');
  const location = ev.dataset.venue || '';
  window.open('https://calendar.google.com/calendar/render?action=TEMPLATE'
    + '&text=' + encodeURIComponent(title)
    + '&dates=' + start + '/' + end
    + '&details=' + encodeURIComponent(desc.trim())
    + '&location=' + encodeURIComponent(location), '_blank');
}}
function addToIcal(ev) {{
  const title = ev.dataset.title;
  const start = toGcalDate(ev.dataset.start);
  const end = toGcalDate(ev.dataset.end);
  const desc = (ev.dataset.desc || '') + '\\n\\n' + (ev.dataset.url || '');
  const location = ev.dataset.venue || '';
  const ics = [
    'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//SXSW//EN','BEGIN:VEVENT',
    'DTSTART:' + start, 'DTEND:' + end,
    'SUMMARY:' + title.replace(/,/g, '\\\\,'),
    'DESCRIPTION:' + desc.replace(/\\n/g, '\\\\n').replace(/,/g, '\\\\,'),
    'LOCATION:' + location.replace(/,/g, '\\\\,'),
    'END:VEVENT','END:VCALENDAR'
  ].join('\\r\\n');
  const blob = new Blob([ics], {{ type: 'text/calendar;charset=utf-8' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = title.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50) + '.ics';
  a.click();
  URL.revokeObjectURL(a.href);
}}

// ── Init ──
['tech', 'innov'].forEach(s => applyFilters(s));
updateFavBtns();
</script>
</body>
</html>'''

with open('/Users/noah/dev/sxsw-tech-ai/index.html', 'w') as f:
    f.write(html)
print(f"Written {len(html)//1024}KB")
print(f"Tech & AI: {n_tech_events} events, {n_tech_speakers} speakers")
print(f"Innovation: {n_innov_events} events, {n_innov_speakers} speakers")
