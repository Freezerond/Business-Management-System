export const formatMeetingTime = (startIso: string, endIso: string) => {
  const start = new Date(startIso);
  const end = new Date(endIso);

  const day = String(start.getDate()).padStart(2, "0");
  const month = String(start.getMonth() + 1).padStart(2, "0");
  const year = start.getFullYear();

  const startHours = String(start.getHours()).padStart(2, "0");
  const startMinutes = String(start.getMinutes()).padStart(2, "0");

  const endHours = String(end.getHours()).padStart(2, "0");
  const endMinutes = String(end.getMinutes()).padStart(2, "0");

  return `${day}.${month}.${year} ${startHours}:${startMinutes} - ${endHours}:${endMinutes}`;
};

