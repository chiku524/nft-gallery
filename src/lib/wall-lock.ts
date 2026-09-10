const SNAP_SLACK = 8;
export const WALL_LOCK_INSET = 16;

let wallEngaged = false;

export function setWallEngaged(engaged: boolean) {
  wallEngaged = engaged;
  if (!engaged) unlockPageScroll();
}

export function isWallEngaged() {
  return wallEngaged;
}

export function snapElementToTop(el: HTMLElement, inset = WALL_LOCK_INSET) {
  const top = el.getBoundingClientRect().top;
  if (Math.abs(top - inset) <= SNAP_SLACK) return true;

  window.scrollTo({
    top: Math.max(0, window.scrollY + top - inset),
    behavior: "auto",
  });

  return Math.abs(el.getBoundingClientRect().top - inset) <= SNAP_SLACK;
}

export function lockPageScroll() {
  wallEngaged = true;
  document.documentElement.style.overflow = "hidden";
  document.body.style.overflow = "hidden";
  document.documentElement.style.overscrollBehavior = "none";
}

export function unlockPageScroll() {
  document.documentElement.style.overflow = "";
  document.body.style.overflow = "";
  document.documentElement.style.overscrollBehavior = "";
}
