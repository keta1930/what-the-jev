/**
 * 按索引分类顺序排列，各组内部按更新时间倒序。
 * @template {{group: string, updatedAt: string, order: number, id: string}} T
 * @param {T[]} entries
 * @param {string[]} groups
 * @returns {T[]}
 */
export function groupEntries(entries, groups) {
  return entries.toSorted(
    (a, b) =>
      groups.indexOf(a.group) - groups.indexOf(b.group) ||
      Date.parse(b.updatedAt) - Date.parse(a.updatedAt) ||
      a.order - b.order ||
      a.id.localeCompare(b.id),
  );
}
