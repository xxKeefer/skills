async function prompt_boolean(tp: Tp, prompt: string, defaultResponse?: string): Promise<boolean> {
  const response = await tp.system.prompt(prompt, defaultResponse);
  if (response === null) return false;
  return ["yes", "y", "true", "1"].includes(response.toLowerCase());
}

export = prompt_boolean;
