import { Component, OnDestroy, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { EMPTY, forkJoin, from, Observable, of } from 'rxjs';
import { catchError, finalize, switchMap } from 'rxjs/operators';
import { SidebarComponent } from '../shared/sidebar.component';
import { TranslateModule } from '@ngx-translate/core';
import {
  ApiService,
  ClockQrStatus,
  WorkSession,
  WorkSessionClockPayload,
  workSessionNetWorkSeconds,
  workSessionOpenExceedsContract,
} from '../services/api.service';

@Component({
  selector: 'app-my-shift',
  standalone: true,
  imports: [CommonModule, SidebarComponent, TranslateModule],
  template: `
    <app-sidebar>
      <div class="my-shift-page" data-testid="my-shift-page">
        <div class="page-header">
          <h1>{{ 'MY_SHIFT.TITLE' | translate }}</h1>
          <p class="subtitle">{{ 'MY_SHIFT.SUBTITLE' | translate }}</p>
        </div>

        <p class="hint">{{ 'MY_SHIFT.AUDIT_HINT' | translate }}</p>

        @if (clockStatus()?.clock_qr_required) {
          <p class="hint qr-hint">{{ 'MY_SHIFT.QR_HINT' | translate }}</p>
        }
        @if (clockStatus()?.clock_qr_location_verify) {
          <p class="hint">{{ 'MY_SHIFT.LOCATION_HINT' | translate }}</p>
        }

        @if (exceedsContract()) {
          <div class="overtime-banner" role="status" data-testid="my-shift-overtime-banner">
            <strong>{{ 'MY_SHIFT.OVERTIME_TITLE' | translate }}</strong>
            <p>{{ 'MY_SHIFT.OVERTIME_BODY' | translate: { hours: contractHours() } }}</p>
          </div>
        }

        @if (error()) {
          <div class="error-banner">{{ error() }}</div>
        }

        @if (qrBlocked()) {
          <div class="error-banner" role="alert">{{ 'MY_SHIFT.ERR_QR' | translate }}</div>
        }

        <section class="card clock-card">
          @if (loading()) {
            <p class="muted">{{ 'MY_SHIFT.LOADING' | translate }}</p>
          } @else if (open(); as s) {
            @if (s.on_break) {
              <p class="status break">{{ 'MY_SHIFT.STATUS_BREAK' | translate }}</p>
            } @else {
              <p class="status on">{{ 'MY_SHIFT.STATUS_ON' | translate }}</p>
            }
            <p class="time-row">
              <span class="label">{{ 'MY_SHIFT.STARTED' | translate }}</span>
              <span>{{ formatDt(s.started_at) }}</span>
            </p>
            @if (openElapsedLabel()) {
              <p class="time-row elapsed-row">
                <span class="label">{{ 'MY_SHIFT.NET_ELAPSED' | translate }}</span>
                <span>{{ openElapsedLabel() }}</span>
              </p>
            }
            <div class="btn-stack">
              @if (s.on_break) {
                <button
                  type="button"
                  class="btn btn-primary"
                  (click)="endBreak()"
                  [disabled]="actionLoading() || qrBlocked()"
                >
                  {{ actionLoading() ? ('MY_SHIFT.WORKING' | translate) : ('MY_SHIFT.END_BREAK' | translate) }}
                </button>
              } @else {
                <button
                  type="button"
                  class="btn btn-secondary"
                  (click)="startBreak()"
                  [disabled]="actionLoading() || qrBlocked()"
                >
                  {{ actionLoading() ? ('MY_SHIFT.WORKING' | translate) : ('MY_SHIFT.START_BREAK' | translate) }}
                </button>
                <button
                  type="button"
                  class="btn btn-primary btn-end"
                  (click)="endShift()"
                  [disabled]="actionLoading() || qrBlocked()"
                >
                  {{ actionLoading() ? ('MY_SHIFT.WORKING' | translate) : ('MY_SHIFT.END_SHIFT' | translate) }}
                </button>
              }
            </div>
          } @else {
            <p class="status off">{{ 'MY_SHIFT.STATUS_OFF' | translate }}</p>
            <button
              type="button"
              class="btn btn-primary"
              (click)="startShift()"
              [disabled]="actionLoading() || qrBlocked()"
            >
              {{ actionLoading() ? ('MY_SHIFT.WORKING' | translate) : ('MY_SHIFT.START_SHIFT' | translate) }}
            </button>
          }
        </section>

        <section class="card history-card">
          <h2>{{ 'MY_SHIFT.HISTORY_TITLE' | translate }}</h2>
          @if (history().length === 0) {
            <p class="muted">{{ 'MY_SHIFT.NO_HISTORY' | translate }}</p>
          } @else {
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>{{ 'MY_SHIFT.COL_START' | translate }}</th>
                    <th>{{ 'MY_SHIFT.COL_END' | translate }}</th>
                    <th>{{ 'MY_SHIFT.COL_DURATION' | translate }}</th>
                  </tr>
                </thead>
                <tbody>
                  @for (row of history(); track row.id) {
                    <tr [class.open-row]="!row.ended_at">
                      <td>{{ formatDt(row.started_at) }}</td>
                      <td>{{ row.ended_at ? formatDt(row.ended_at) : '—' }}</td>
                      <td>{{ formatDuration(row) }}</td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>
          }
        </section>
      </div>
    </app-sidebar>
  `,
  styles: `
    .my-shift-page {
      max-width: 720px;
    }
    .page-header h1 {
      margin: 0 0 0.25rem;
      font-size: 1.5rem;
    }
    .subtitle {
      margin: 0 0 1rem;
      color: var(--color-text-muted, #666);
      font-size: 0.9375rem;
    }
    .hint {
      font-size: 0.8125rem;
      color: var(--color-text-muted, #666);
      margin: 0 0 1.25rem;
      line-height: 1.4;
    }
    .qr-hint {
      margin-bottom: 0.5rem;
    }
    .error-banner {
      background: var(--color-danger-bg, #fde8e8);
      color: var(--color-danger, #b91c1c);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
    }
    .overtime-banner {
      background: var(--color-warning-bg, #fff8e6);
      border: 1px solid var(--color-warning-border, #f5d78e);
      color: var(--color-text, #1a1a1a);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
    }
    .overtime-banner strong {
      display: block;
      margin-bottom: 0.35rem;
    }
    .overtime-banner p {
      margin: 0;
      font-size: 0.875rem;
      line-height: 1.45;
    }
    .card {
      background: var(--color-surface, #fff);
      border: 1px solid var(--color-border, #e5e5e5);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
    }
    .clock-card .status {
      font-weight: 600;
      margin: 0 0 0.75rem;
    }
    .clock-card .status.on {
      color: var(--color-success, #15803d);
    }
    .clock-card .status.break {
      color: var(--color-warning-text, #b45309);
    }
    .clock-card .status.off {
      color: var(--color-text-muted, #666);
    }
    .time-row {
      margin: 0 0 1rem;
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .time-row .label {
      color: var(--color-text-muted, #666);
    }
    .btn-stack {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      align-items: stretch;
    }
    .btn-stack .btn {
      min-height: 48px;
      font-size: 1rem;
    }
    .btn-end {
      margin-top: 0;
    }
    .history-card h2 {
      margin: 0 0 1rem;
      font-size: 1.125rem;
    }
    .muted {
      color: var(--color-text-muted, #666);
      margin: 0;
    }
    .table-wrap {
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
    }
    th,
    td {
      text-align: left;
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--color-border, #eee);
    }
    th {
      font-weight: 600;
      color: var(--color-text-muted, #666);
    }
    .open-row {
      background: var(--color-highlight-bg, #f0f9ff);
    }
  `,
})
export class MyShiftComponent implements OnInit, OnDestroy {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  loading = signal(true);
  actionLoading = signal(false);
  error = signal<string | null>(null);
  open = signal<WorkSession | null>(null);
  history = signal<WorkSession[]>([]);
  clockStatus = signal<ClockQrStatus | null>(null);
  /** From ?clock_qr= only; persisted to sessionStorage in ngOnInit */
  clockQrToken = signal<string | null>(null);

  private overtimeTick = signal(0);
  private overtimeTimer: ReturnType<typeof setInterval> | null = null;
  private querySub: { unsubscribe: () => void } | null = null;

  exceedsContract = computed(() => {
    this.overtimeTick();
    return workSessionOpenExceedsContract(this.open());
  });

  contractHours = computed(() => {
    const m = this.open()?.contract_threshold_minutes ?? 480;
    return Math.round(m / 60);
  });

  qrBlocked = computed(() => {
    const st = this.clockStatus();
    if (!st?.clock_qr_required) return false;
    const u = this.api.getCurrentUser();
    const tid = u?.tenant_id;
    const fromUrl = this.clockQrToken();
    const stored = tid != null ? sessionStorage.getItem(`clock_qr_${tid}`) : null;
    const token = (fromUrl || stored || '').trim();
    return !token;
  });

  openElapsedLabel = computed(() => {
    this.overtimeTick();
    const s = this.open();
    if (!s || s.ended_at) return '';
    const sec = workSessionNetWorkSeconds(s);
    const mins = Math.max(0, Math.floor(sec / 60));
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
  });

  ngOnInit(): void {
    this.querySub = this.route.queryParamMap.subscribe((q) => {
      const t = q.get('clock_qr');
      if (t?.trim()) {
        this.clockQrToken.set(t.trim());
        const u = this.api.getCurrentUser();
        const tid = u?.tenant_id;
        if (tid != null) {
          sessionStorage.setItem(`clock_qr_${tid}`, t.trim());
        }
        this.router.navigate([], {
          relativeTo: this.route,
          queryParams: { clock_qr: null },
          queryParamsHandling: 'merge',
          replaceUrl: true,
        });
      }
    });
    this.refreshAll();
    this.overtimeTimer = setInterval(() => this.overtimeTick.update((n) => n + 1), 1000);
  }

  ngOnDestroy(): void {
    this.querySub?.unsubscribe();
    if (this.overtimeTimer != null) {
      clearInterval(this.overtimeTimer);
      this.overtimeTimer = null;
    }
  }

  private rangeLastDays(n: number): { from: string; to: string } {
    const to = new Date();
    const from = new Date(to);
    from.setDate(from.getDate() - n);
    return { from: from.toISOString().slice(0, 10), to: to.toISOString().slice(0, 10) };
  }

  private effectiveClockQr(): string | undefined {
    const u = this.api.getCurrentUser();
    const tid = u?.tenant_id;
    const t =
      (this.clockQrToken() || (tid != null ? sessionStorage.getItem(`clock_qr_${tid}`) : null) || '').trim();
    return t || undefined;
  }

  private buildClockPayload(): Observable<WorkSessionClockPayload> {
    const st = this.clockStatus();
    const payload: WorkSessionClockPayload = {};
    const q = this.effectiveClockQr();
    if (q) payload.clock_qr = q;
    if (st?.clock_qr_location_verify) {
      return from(
        new Promise<WorkSessionClockPayload>((resolve, reject) => {
          if (!('geolocation' in navigator)) {
            reject(new Error('no geolocation'));
            return;
          }
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              resolve({
                ...payload,
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
              });
            },
            () => reject(new Error('geo denied')),
            { timeout: 15000, maximumAge: 120000 }
          );
        })
      ).pipe(
        catchError(() => {
          this.error.set(
            'Location is required for clock actions at this venue. Allow access in your browser and try again.'
          );
          return EMPTY;
        })
      );
    }
    return of(payload);
  }

  refreshAll(): void {
    this.loading.set(true);
    this.error.set(null);
    const { from, to } = this.rangeLastDays(30);
    forkJoin({
      open: this.api.getMyOpenWorkSession(),
      history: this.api.getMyWorkSessions(from, to),
      qr: this.api.getMyClockQrStatus(),
    }).subscribe({
      next: ({ open, history, qr }) => {
        this.open.set(open);
        this.history.set(history);
        this.clockStatus.set(qr);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Could not load shift data');
      },
    });
  }

  startShift(): void {
    this.actionLoading.set(true);
    this.error.set(null);
    this.buildClockPayload()
      .pipe(
        switchMap((payload) => this.api.startMyWorkSession(payload)),
        finalize(() => this.actionLoading.set(false))
      )
      .subscribe({
        next: (s) => {
          this.open.set(s);
          this.refreshHistoryOnly();
        },
        error: (err) => {
          this.error.set(err?.error?.detail || 'Could not start shift');
        },
      });
  }

  endShift(): void {
    this.actionLoading.set(true);
    this.error.set(null);
    this.buildClockPayload()
      .pipe(
        switchMap((payload) => this.api.endMyWorkSession(payload)),
        finalize(() => this.actionLoading.set(false))
      )
      .subscribe({
        next: () => {
          this.open.set(null);
          this.refreshHistoryOnly();
        },
        error: (err) => {
          this.error.set(err?.error?.detail || 'Could not end shift');
        },
      });
  }

  startBreak(): void {
    this.actionLoading.set(true);
    this.error.set(null);
    this.api.startMyWorkSessionBreak().subscribe({
      next: (s) => {
        this.open.set(s);
        this.actionLoading.set(false);
        this.refreshHistoryOnly();
      },
      error: (err) => {
        this.actionLoading.set(false);
        this.error.set(err?.error?.detail || 'Could not start break');
      },
    });
  }

  endBreak(): void {
    this.actionLoading.set(true);
    this.error.set(null);
    this.buildClockPayload()
      .pipe(
        switchMap((payload) => this.api.endMyWorkSessionBreak(payload)),
        finalize(() => this.actionLoading.set(false))
      )
      .subscribe({
        next: (s) => {
          this.open.set(s);
          this.refreshHistoryOnly();
        },
        error: (err) => {
          const d = err?.error?.detail;
          this.error.set(
            typeof d === 'string' && d.toLowerCase().includes('qr')
              ? 'Scan the venue QR code (or use the staff link with the token) to end your break.'
              : d || 'Could not end break'
          );
        },
      });
  }

  private refreshHistoryOnly(): void {
    const { from, to } = this.rangeLastDays(30);
    this.api.getMyWorkSessions(from, to).subscribe({
      next: (rows) => this.history.set(rows),
      error: () => {},
    });
  }

  formatDt(iso: string): string {
    const d = new Date(iso);
    return isNaN(d.getTime()) ? iso : d.toLocaleString();
  }

  formatDuration(row: WorkSession): string {
    if (row.duration_minutes != null && row.duration_minutes >= 0) {
      const h = Math.floor(row.duration_minutes / 60);
      const m = row.duration_minutes % 60;
      if (h > 0) return `${h}h ${m}m`;
      return `${m}m`;
    }
    if (!row.ended_at) return '…';
    return '—';
  }
}
