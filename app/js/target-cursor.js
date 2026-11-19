/* TargetCursor disabled for silky smooth native 120Hz Apple interaction */
(function () {
  "use strict";
  function cleanup() {
    const root = document.getElementById("rb-target-cursor");
    if (root) root.remove();
    const style = document.getElementById("rb-target-cursor-styles");
    if (style) style.remove();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", cleanup);
  } else {
    cleanup();
  }
})();
