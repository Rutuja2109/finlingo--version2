// Course titles are stored as "Name: subtitle". Where the name is already shown, show only the subtitle.
export function courseSubtitle(course) {
  const title = course?.title || "";
  const name = course?.name || "";
  return name && title.startsWith(`${name}: `) ? title.slice(name.length + 2) : title;
}
