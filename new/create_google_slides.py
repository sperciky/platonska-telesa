#!/usr/bin/env python3
"""
Vytvoří Google Slides prezentaci s GIF animacemi z tutoriálu Platónských těles.
Creates a Google Slides presentation with GIF animations from the Platonic solids tutorial.

══════════════════════════════════════════════════════════════════════════════
 SETUP (one-time)
══════════════════════════════════════════════════════════════════════════════
 1. Go to  https://console.cloud.google.com
 2. Create (or select) a project.
 3. Enable these two APIs:
      • Google Slides API
      • Google Drive API
 4. Go to  APIs & Services → Credentials → Create Credentials → OAuth client ID
      • Application type: Desktop app
      • Download the JSON → save as  credentials.json  next to this script.
 5. Install Python packages:
      pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

 The first run opens a browser for you to authorise the app (one-time).
 After that a  token.json  is saved and reused automatically.

══════════════════════════════════════════════════════════════════════════════
 USAGE
══════════════════════════════════════════════════════════════════════════════
 cd new/
 python generate_animations.py        # creates animations/ folder first
 python create_google_slides.py       # uploads to Google Slides

 Optional flags:
   --title "My presentation title"
   --animdir  path/to/animations/     # default: animations/
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print(
        "Google API libraries not found. Install them with:\n"
        "  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib\n"
    )
    sys.exit(1)

# ── Constants ─────────────────────────────────────────────────────────────────
_HERE = Path(__file__).resolve().parent

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file',
]

CREDENTIALS_FILE = _HERE / 'credentials.json'
TOKEN_FILE       = _HERE / 'token.json'

# Google Slides uses EMU (English Metric Units): 1 inch = 914400 EMU
# Standard widescreen slide: 10 × 5.625 inches
SLIDE_W = 9144000   # 10 in
SLIDE_H = 5143500   # 5.625 in

# Layout geometry (all in EMU)
TITLE_X, TITLE_Y = 457200,  228600          # 0.5 in, 0.25 in
TITLE_W, TITLE_H = 8229600, 685800          # 9 in wide, 0.75 in tall
IMAGE_X, IMAGE_Y = 228600,  1028700         # 0.25 in, 1.125 in
IMAGE_W, IMAGE_H = 4800000, 4000000         # ~5.25 in, ~4.37 in
DESC_X,  DESC_Y  = 5257200, 1028700         # right column
DESC_W,  DESC_H  = 3657600, 4000000         # ~4 in wide

# Title slide geometry
COVER_TITLE_Y = 1600000
COVER_TITLE_H = 1200000
COVER_SUB_Y   = 2900000
COVER_SUB_H   =  600000

# ── Palette for slide backgrounds (cycles through step categories) ─────────────
_CATEGORY_COLORS = {
    'Čtyřstěn':    {'r': 0.95, 'g': 0.92, 'b': 0.85},  # warm cream
    'Osmistěn':    {'r': 0.88, 'g': 0.93, 'b': 0.98},  # light blue
    'Dvacetistěn': {'r': 0.90, 'g': 0.97, 'b': 0.90},  # light green
    'Dvanáctistěn':{'r': 0.97, 'g': 0.90, 'b': 0.97},  # light purple
    'Dualita':     {'r': 0.99, 'g': 0.95, 'b': 0.88},  # light gold
    'BONUS':       {'r': 0.97, 'g': 0.97, 'b': 0.80},  # pale yellow
}
_DEFAULT_BG = {'r': 0.98, 'g': 0.98, 'b': 0.98}


def _bg_for_title(title: str) -> dict:
    for key, color in _CATEGORY_COLORS.items():
        if key in title:
            return color
    return _DEFAULT_BG


# ── Google auth ───────────────────────────────────────────────────────────────

def get_credentials() -> Credentials:
    """Return valid Google OAuth credentials, refreshing or re-authorising as needed."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"\ncredentials.json not found at:\n  {CREDENTIALS_FILE}\n\n"
                    "Download it from:\n"
                    "  Google Cloud Console → APIs & Services → Credentials\n"
                    "  → Create Credentials → OAuth client ID (Desktop app)\n"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
            f.write(creds.to_json())

    return creds


# ── Drive helpers ─────────────────────────────────────────────────────────────

def upload_gif(drive_service, gif_path: Path) -> str:
    """
    Upload a GIF to Google Drive and return a publicly readable URL.

    Google Slides API requires images to be served over HTTP(S). Uploading
    to Drive and making the file public is the simplest way to achieve this
    without needing your own hosting.
    """
    print(f"    uploading {gif_path.name} …", end=' ', flush=True)

    file_meta = {'name': gif_path.name, 'mimeType': 'image/gif'}
    media     = MediaFileUpload(str(gif_path), mimetype='image/gif', resumable=False)

    file = drive_service.files().create(
        body=file_meta, media_body=media, fields='id'
    ).execute()
    file_id = file['id']

    # Make publicly readable (anyone with link)
    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"ok  ({url[-30:]})")
    return url


# ── Slide builder helpers ─────────────────────────────────────────────────────

def _emu(val: int) -> dict:
    return {'magnitude': val, 'unit': 'EMU'}


def _rgb(r: float, g: float, b: float) -> dict:
    return {'red': r, 'green': g, 'blue': b}


def _text_style_request(obj_id: str, bold: bool, size_pt: int,
                        r: float, g: float, b: float) -> dict:
    return {
        'updateTextStyle': {
            'objectId': obj_id,
            'style': {
                'bold': bold,
                'fontSize': {'magnitude': size_pt, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': _rgb(r, g, b)}},
            },
            'textRange': {'type': 'ALL'},
            'fields': 'bold,fontSize,foregroundColor',
        }
    }


def _para_align_request(obj_id: str, alignment: str = 'CENTER') -> dict:
    return {
        'updateParagraphStyle': {
            'objectId': obj_id,
            'style': {'alignment': alignment},
            'textRange': {'type': 'ALL'},
            'fields': 'alignment',
        }
    }


def add_cover_slide(slides_service, presentation_id: str,
                    existing_slide_id: str, title: str) -> None:
    """Repurpose the default blank slide as a cover slide."""
    title_id = 'cover_title'
    sub_id   = 'cover_sub'
    requests = [
        # Set background colour
        {
            'updatePageProperties': {
                'objectId': existing_slide_id,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'solidFill': {'color': {'rgbColor': _rgb(0.15, 0.20, 0.40)}}
                    }
                },
                'fields': 'pageBackgroundFill',
            }
        },
        # Main title text box
        {
            'createShape': {
                'objectId': title_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': existing_slide_id,
                    'size': {'width': _emu(7315200), 'height': _emu(COVER_TITLE_H)},
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': 914400, 'translateY': COVER_TITLE_Y,
                        'unit': 'EMU',
                    },
                },
            }
        },
        {'insertText': {'objectId': title_id, 'text': title, 'insertionIndex': 0}},
        _text_style_request(title_id, bold=True,  size_pt=40, r=1, g=1, b=1),
        _para_align_request(title_id, 'CENTER'),
        # Subtitle
        {
            'createShape': {
                'objectId': sub_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': existing_slide_id,
                    'size': {'width': _emu(7315200), 'height': _emu(COVER_SUB_H)},
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': 914400, 'translateY': COVER_SUB_Y,
                        'unit': 'EMU',
                    },
                },
            }
        },
        {
            'insertText': {
                'objectId': sub_id,
                'text': 'Interaktivní tutoriál pro 3D geometrii',
                'insertionIndex': 0,
            }
        },
        _text_style_request(sub_id, bold=False, size_pt=22, r=0.8, g=0.85, b=1.0),
        _para_align_request(sub_id, 'CENTER'),
    ]
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={'requests': requests}
    ).execute()


def add_content_slide(slides_service, presentation_id: str,
                      insertion_index: int, step_title: str,
                      gif_url: str) -> str:
    """
    Insert a new slide at insertion_index with:
      - coloured background matching the step category
      - large title at the top
      - animated GIF on the left
      - empty right column (space for notes / future text)

    Returns the new slide's objectId.
    """
    bg = _bg_for_title(step_title)

    # Step 1: insert blank slide
    resp = slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={
            'requests': [{
                'insertSlide': {
                    'insertionIndex': insertion_index,
                    'slideLayoutReference': {'predefinedLayout': 'BLANK'},
                }
            }]
        }
    ).execute()
    slide_id = resp['replies'][0]['insertSlide']['objectId']

    title_id = f"title_{insertion_index}"
    image_id = f"image_{insertion_index}"

    requests = [
        # Background
        {
            'updatePageProperties': {
                'objectId': slide_id,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'solidFill': {'color': {'rgbColor': _rgb(**bg)}}
                    }
                },
                'fields': 'pageBackgroundFill',
            }
        },
        # Title text box
        {
            'createShape': {
                'objectId': title_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': _emu(TITLE_W), 'height': _emu(TITLE_H)},
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': TITLE_X, 'translateY': TITLE_Y,
                        'unit': 'EMU',
                    },
                },
            }
        },
        {'insertText': {'objectId': title_id, 'text': step_title, 'insertionIndex': 0}},
        _text_style_request(title_id, bold=True, size_pt=22, r=0.1, g=0.1, b=0.3),
        # GIF image
        {
            'createImage': {
                'objectId': image_id,
                'url': gif_url,
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': _emu(IMAGE_W), 'height': _emu(IMAGE_H)},
                    'transform': {
                        'scaleX': 1, 'scaleY': 1,
                        'translateX': IMAGE_X, 'translateY': IMAGE_Y,
                        'unit': 'EMU',
                    },
                },
            }
        },
    ]

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={'requests': requests}
    ).execute()
    return slide_id


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Create a Google Slides presentation from GIF animations.'
    )
    parser.add_argument('--title',    default='Platónská tělesa – Interaktivní tutoriál',
                        help='Presentation title (default: Platónská tělesa …)')
    parser.add_argument('--animdir',  default='animations',
                        help='Folder containing GIFs (default: animations/)')
    args = parser.parse_args()

    anim_dir  = _HERE / args.animdir
    meta_file = anim_dir / '_metadata.json'

    # ── Load metadata produced by generate_animations.py ─────────────────────
    if meta_file.exists():
        with open(meta_file, encoding='utf-8') as f:
            metadata = json.load(f)          # list of [step_num, title, gif_rel_path]
        gif_entries = [
            (num, title, _HERE / rel_path)
            for num, title, rel_path in metadata
            if (_HERE / rel_path).exists()
        ]
    else:
        # Fallback: just sort GIFs alphabetically
        gif_files = sorted(anim_dir.glob('step_*.gif'))
        if not gif_files:
            print(f"No GIF files found in {anim_dir}")
            print("Run  python generate_animations.py  first!")
            sys.exit(1)
        gif_entries = [(i, p.stem, p) for i, p in enumerate(gif_files)]

    if not gif_entries:
        print("No valid GIF entries found. Run generate_animations.py first.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Platonic Solids – Google Slides Creator")
    print(f"  {len(gif_entries)} slides to create")
    print(f"{'='*60}\n")

    # ── Authenticate ─────────────────────────────────────────────────────────
    print("Authenticating with Google …")
    creds = get_credentials()

    slides_svc = build('slides', 'v1', credentials=creds)
    drive_svc  = build('drive',  'v3', credentials=creds)
    print("  ✓ authenticated\n")

    # ── Create presentation ───────────────────────────────────────────────────
    print(f"Creating presentation: "{args.title}" …")
    presentation = slides_svc.presentations().create(
        body={'title': args.title}
    ).execute()
    pres_id           = presentation['presentationId']
    default_slide_id  = presentation['slides'][0]['objectId']
    print(f"  ✓ https://docs.google.com/presentation/d/{pres_id}/edit\n")

    # ── Cover slide ───────────────────────────────────────────────────────────
    print("Building cover slide …")
    add_cover_slide(slides_svc, pres_id, default_slide_id, args.title)
    print("  ✓ cover slide done\n")

    # ── Content slides ────────────────────────────────────────────────────────
    for slide_index, (step_num, step_title, gif_path) in enumerate(gif_entries, start=1):
        print(f"[{step_index}/{len(gif_entries)}] {step_title}")

        # Upload GIF to Drive
        gif_url = upload_gif(drive_svc, gif_path)

        # Insert slide
        add_content_slide(slides_svc, pres_id, slide_index, step_title, gif_url)
        print(f"    ✓ slide added\n")

        time.sleep(0.4)   # stay within API rate limits

    # ── Done ─────────────────────────────────────────────────────────────────
    print(f"{'='*60}")
    print(f"  ✅  Presentation ready!")
    print(f"  URL: https://docs.google.com/presentation/d/{pres_id}/edit")
    print(f"{'='*60}\n")
    print("Tip: In Google Slides, animated GIFs play automatically")
    print("     in Presentation mode (Ctrl+F5 / Cmd+Enter).\n")

    # Save the URL locally for convenience
    url_file = _HERE / 'google_slides_url.txt'
    url_file.write_text(
        f"https://docs.google.com/presentation/d/{pres_id}/edit\n",
        encoding='utf-8',
    )
    print(f"URL also saved to: {url_file.name}\n")


if __name__ == '__main__':
    main()
