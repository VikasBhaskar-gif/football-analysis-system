# Analyst Desk Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Apply the selected analyst desk design to the running football app.

**Architecture:** Retain existing React components and API calls. Replace the application shell and empty state, with a scoped stylesheet for the shared theme.

**Tech Stack:** React, CSS, Vite, existing lucide icons.

**Spec:** docs/superpowers/specs/2026-10-25-analyst-desk-design.md

## Global Constraints
- Add no dependencies or backend changes.
- Preserve upload, playback, selection and analysis flows.
- Use warm gray, charcoal and restrained forest green.
- Keep dark video/pitch canvases.

## Review Focus
- Empty match catalog must have useful import guidance and no empty selector.
- 375–566px panes must not overflow horizontally.
- Uploaded video must retain playback and timeline controls.
- File picker must be reachable by keyboard and upload feedback must be announced.
- Loaded match views must have readable text and useful navigation.

### Task 1: Shell, import workflow and shared theme
**Files:** App.jsx, components/UploadPromptView.jsx, main.jsx, analyst-desk.css, index.html; small labels in existing workspace components.
**Interfaces:** Existing upload/selection callbacks and backend endpoints remain unchanged.
- [ ] Replace the shell with responsive navigation and conditional match tools.
- [ ] Replace the upload view with accessible import controls and concise workflow guidance.
- [ ] Add light theme and harmonize the loaded workspace, preserving dark media canvases.
- [ ] Build with npm run build. Expected: successful Vite production build.
- [ ] Inspect empty state in browser at embedded and desktop widths. Expected: no clipping, readable hierarchy.
- [ ] Upload a temporary generated video and exercise playback/navigation. Expected: usable loaded workspace.
- [ ] Review changes and reload the running app.

Verification uses build and browser checks for this reversible visual change; no redundant implementation-mirroring tests. No commit requested.
