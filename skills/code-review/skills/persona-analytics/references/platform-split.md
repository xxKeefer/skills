# Platform split

### F. Platform split

25. **Frontend code sending to Segment (Nit).** A frontend import or call of a Segment client (`@segment/*`, `analytics.js`, `window.analytics.track`) where the project's recorded split sends frontend interactions to PostHog through the wrapper and feeds Segment only from backend services, when Marketing asks for it. Check `CLAUDE.md`, ADRs or the wrapper's README for the split. Skip this rule if none is recorded.
