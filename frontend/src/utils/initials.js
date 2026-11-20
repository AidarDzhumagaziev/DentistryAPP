export function initials(fullName) {
  return fullName
    .split(' ')
    .map((part) => part[0])
    .join('');
}