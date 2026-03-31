import { Injectable, signal } from '@angular/core';

/**
 * Tablet-oriented layout: collapse the main nav sidebar and toggle browser fullscreen
 * for Orders / Tables flows.
 */
@Injectable({ providedIn: 'root' })
export class StaffLayoutService {
  /** When true, main sidebar is hidden (desktop/tablet) so content uses full width. */
  readonly sidebarCollapsed = signal(false);

  readonly fullscreenActive = signal(false);

  constructor() {
    if (typeof document !== 'undefined') {
      document.addEventListener('fullscreenchange', () => {
        this.fullscreenActive.set(!!document.fullscreenElement);
      });
    }
  }

  toggleSidebarCollapsed(): void {
    this.sidebarCollapsed.update(v => !v);
  }

  toggleFullscreen(): void {
    if (typeof document === 'undefined') return;
    const el = document.documentElement;
    if (!document.fullscreenElement) {
      void el.requestFullscreen?.().catch(() => {});
    } else {
      void document.exitFullscreen?.().catch(() => {});
    }
  }
}
