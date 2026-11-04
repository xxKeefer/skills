# Stack facts

Stack facts to use in fixes:
- The design system's form component wraps vee-validate and renders a native `<form @submit.prevent>`. Enter submits only if a submit button sits inside it. Check the project's own form component.
- The design system's button renders `type="button"` unless given `type="submit"`. Check the project's own button.
- The design system's input takes `type="number"`; there may be no number-field component. Its attributes pass through to the native `<input>`.
- Validation can differ by app: zod through `toTypedSchema`, or yup. Check which the app uses.
- Share length constants between create and edit so the two agree.
