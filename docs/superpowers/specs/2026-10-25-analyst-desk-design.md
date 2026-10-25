# Analyst desk

Selected direction: Analyst desk, chosen by the user after reviewing the alternatives.

Intent: turn the football analysis app into a focused, calm working tool.

Design: warm gray canvas, white panels, charcoal type, a restrained forest green accent, and thin structural rules. Replace the glowing badge/header and marketing feature cards with compact navigation and a clear import workflow. Use an editorial heading with useful, honest empty-state guidance. Match controls appear when a video is loaded. Keep the video and pitch canvases dark for legibility.

Approaches: the chosen light analyst desk improves hierarchy and scanning; the alternative dark editing suite supports sustained video editing but was not selected.

Constraints: retain React, Vite, current API contracts, uploads, video playback, timeline, player selection and analysis. Add no dependencies. No invented match data or metrics. No backend changes. Responsive at narrow embedded-browser widths and desktop widths.

Implementation choices: reuse existing analysis components; isolate the theme in analyst-desk.css; simplify header and empty-state markup. Keep the source checkout and local server in place.

Verification: production build, browser inspection of empty and uploaded-video states, keyboard file-picker access, and overflow checks at narrow and wide sizes.
