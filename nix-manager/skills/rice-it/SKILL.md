---
name: rice-it
description: >
  Customize the visual appearance of desktop components. Accepts screenshots, text descriptions,
  repo links, or any combination. Use when user says "rice my X", "make X look like Y",
  "I want my desktop to look like this".
---

# Rice It

Visual customization of desktop components. The user provides a target (what to rice) and a
goal (what it should look like) via screenshots, descriptions, repo links, or any mix.

## Step 1: Parse Inputs

`$ARGUMENTS` may contain any combination of:
- **Screenshot path** -- a file path to an image showing the desired look
- **Text description** -- "catppuccin mocha, rounded corners, transparent background"
- **Repo link** -- a URL to someone's dotfiles for inspiration
- **Component** -- what to rice (waybar, terminal, niri, notifications, etc.)

If the target component is unclear, ask.

Read screenshots via the Read tool. Fetch repo links via web. Parse text directly.

**Done when:** target component and visual goal are both clear.

## Step 2: Analyse the Goal

- **Screenshot:** identify colours (hex values), layout, spacing, fonts, visible widgets,
  border radius, transparency, padding, alignment.
- **Repo link:** fetch and study their config for the relevant component. Note patterns,
  colour schemes, layout choices.
- **Text:** clarify ambiguities if any.

Combine all inputs into a coherent visual target.

**Done when:** visual target is concrete enough to implement.

## Step 3: Read Current Config

Explore the user's current config for the target component. Understand:
- Where the config lives (which files)
- Current theme/palette in use
- Existing customizations
- Whether a theme framework (catppuccin, gruvbox, stylix, etc.) is in use

**Done when:** current state is understood.

## Step 4: Propose Changes

Describe what will change visually before writing any code:
- Colours changing from X to Y
- Layout adjustments
- New widgets or elements
- Fonts or spacing changes

Ask user to confirm direction.

**Done when:** user approves the direction.

## Step 5: Write Config

For CSS-heavy components (waybar): write the style changes.
For nix-configured components: write the nix.
For mixed: handle both.

If the existing config is messy, clean it up while ricing -- restructuring is welcome.

If a colour scheme framework is in use, stay within it unless explicitly asked to change.

**Done when:** config is written.

## Step 6: Explain

Post-edit, explain:
- Colour values chosen and why
- Layout decisions
- Font choices
- Any restructuring done

**Done when:** user acknowledges.

## Step 7: Rebuild and Review

Offer to rebuild so the user can see the result.

After rebuild, ask: "How does it look? Adjust, or done?"

Loop back to Step 4 if adjustments needed.

**Done when:** user says done.

## Principles

- Respect the existing theme/palette unless explicitly asked to change it.
- If a theme framework is detected, stay within it.
- Restructuring messy config while ricing is encouraged.
- The loop (propose -> write -> review -> adjust) is the core of this skill. Iterate until right.
