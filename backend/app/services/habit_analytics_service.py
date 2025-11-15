"""
Service for habit analytics, streak tracking, and insights.
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple
from uuid import UUID
import calendar

from fastapi import HTTPException, status
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit, HabitEntry
from app.schemas.habit_analytics import (
    StreakInfo,
    CompletionStats,
    HabitAnalytics,
    DailyCompletionData,
    WeeklyProgress,
    MonthlyProgress,
    ProgressTrends,
    StreakRecoveryInfo,
    HabitInsights,
)


class HabitAnalyticsService:
    """Service for habit analytics and streak calculations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_streak(self, habit_id: UUID, user_id: UUID) -> StreakInfo:
        """
        Calculate streak information for a habit.
        Handles daily, weekly, and monthly frequencies.
        """
        # Get habit
        habit_result = await self.db.execute(
            select(Habit).where(and_(Habit.id == habit_id, Habit.user_id == user_id))
        )
        habit = habit_result.scalar_one_or_none()
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
            )

        # Get all completed entries, sorted by date descending
        entries_result = await self.db.execute(
            select(HabitEntry)
            .where(
                and_(HabitEntry.habit_id == habit_id, HabitEntry.completed == True)
            )
            .order_by(HabitEntry.entry_date.desc())
        )
        completed_entries = list(entries_result.scalars().all())

        if not completed_entries:
            return StreakInfo(
                current_streak=0,
                longest_streak=0,
                last_completed_date=None,
                is_active=False,
                streak_start_date=None,
            )

        # Calculate streaks based on frequency
        if habit.frequency == "daily":
            return self._calculate_daily_streak(completed_entries)
        elif habit.frequency == "weekly":
            return self._calculate_weekly_streak(completed_entries)
        else:  # monthly or custom
            return self._calculate_monthly_streak(completed_entries)

    def _calculate_daily_streak(
        self, completed_entries: List[HabitEntry]
    ) -> StreakInfo:
        """Calculate streak for daily habits."""
        if not completed_entries:
            return StreakInfo(
                current_streak=0,
                longest_streak=0,
                last_completed_date=None,
                is_active=False,
                streak_start_date=None,
            )

        today = date.today()
        last_completed = completed_entries[0].entry_date
        
        # Check if streak is active (completed today or yesterday)
        days_since_last = (today - last_completed).days
        is_active = days_since_last <= 1

        # Calculate current streak
        current_streak = 0
        streak_start_date = None
        expected_date = last_completed

        for entry in completed_entries:
            if entry.entry_date == expected_date or (
                expected_date - entry.entry_date
            ).days == 0:
                if current_streak == 0:
                    streak_start_date = entry.entry_date
                current_streak += 1
                expected_date = entry.entry_date - timedelta(days=1)
            else:
                break

        # Calculate longest streak
        longest_streak = 1
        temp_streak = 1
        prev_date = completed_entries[0].entry_date

        for i in range(1, len(completed_entries)):
            current_date = completed_entries[i].entry_date
            if (prev_date - current_date).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
            prev_date = current_date

        return StreakInfo(
            current_streak=current_streak,
            longest_streak=longest_streak,
            last_completed_date=last_completed,
            is_active=is_active,
            streak_start_date=streak_start_date,
        )

    def _calculate_weekly_streak(
        self, completed_entries: List[HabitEntry]
    ) -> StreakInfo:
        """Calculate streak for weekly habits."""
        if not completed_entries:
            return StreakInfo(
                current_streak=0,
                longest_streak=0,
                last_completed_date=None,
                is_active=False,
                streak_start_date=None,
            )

        today = date.today()
        last_completed = completed_entries[0].entry_date

        # Group entries by week
        weeks = {}
        for entry in completed_entries:
            week_start = entry.entry_date - timedelta(days=entry.entry_date.weekday())
            if week_start not in weeks:
                weeks[week_start] = []
            weeks[week_start].append(entry)

        sorted_weeks = sorted(weeks.keys(), reverse=True)
        
        # Check if current week is active
        current_week_start = today - timedelta(days=today.weekday())
        is_active = sorted_weeks and sorted_weeks[0] == current_week_start

        # Calculate current streak
        current_streak = 0
        streak_start_date = None
        expected_week = sorted_weeks[0] if sorted_weeks else None

        for week_start in sorted_weeks:
            if expected_week and week_start == expected_week:
                if current_streak == 0:
                    streak_start_date = weeks[week_start][0].entry_date
                current_streak += 1
                expected_week = week_start - timedelta(weeks=1)
            else:
                break

        # Calculate longest streak
        longest_streak = 1
        temp_streak = 1

        for i in range(1, len(sorted_weeks)):
            if (sorted_weeks[i - 1] - sorted_weeks[i]).days == 7:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1

        return StreakInfo(
            current_streak=current_streak,
            longest_streak=longest_streak,
            last_completed_date=last_completed,
            is_active=is_active,
            streak_start_date=streak_start_date,
        )

    def _calculate_monthly_streak(
        self, completed_entries: List[HabitEntry]
    ) -> StreakInfo:
        """Calculate streak for monthly habits."""
        if not completed_entries:
            return StreakInfo(
                current_streak=0,
                longest_streak=0,
                last_completed_date=None,
                is_active=False,
                streak_start_date=None,
            )

        today = date.today()
        last_completed = completed_entries[0].entry_date

        # Group entries by month
        months = {}
        for entry in completed_entries:
            month_key = (entry.entry_date.year, entry.entry_date.month)
            if month_key not in months:
                months[month_key] = []
            months[month_key].append(entry)

        sorted_months = sorted(months.keys(), reverse=True)
        
        # Check if current month is active
        current_month = (today.year, today.month)
        is_active = sorted_months and sorted_months[0] == current_month

        # Calculate current streak
        current_streak = 0
        streak_start_date = None
        expected_month = sorted_months[0] if sorted_months else None

        for month_key in sorted_months:
            if expected_month and month_key == expected_month:
                if current_streak == 0:
                    streak_start_date = months[month_key][0].entry_date
                current_streak += 1
                # Calculate previous month
                year, month = month_key
                if month == 1:
                    expected_month = (year - 1, 12)
                else:
                    expected_month = (year, month - 1)
            else:
                break

        # Calculate longest streak
        longest_streak = 1
        temp_streak = 1

        for i in range(1, len(sorted_months)):
            year_curr, month_curr = sorted_months[i - 1]
            year_prev, month_prev = sorted_months[i]
            
            # Check if consecutive months
            if month_curr == 1:
                expected_prev = (year_curr - 1, 12)
            else:
                expected_prev = (year_curr, month_curr - 1)
            
            if (year_prev, month_prev) == expected_prev:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1

        return StreakInfo(
            current_streak=current_streak,
            longest_streak=longest_streak,
            last_completed_date=last_completed,
            is_active=is_active,
            streak_start_date=streak_start_date,
        )

    async def get_completion_stats(
        self, habit_id: UUID, user_id: UUID
    ) -> CompletionStats:
        """Get completion statistics for a habit."""
        # Verify habit ownership
        habit_result = await self.db.execute(
            select(Habit).where(and_(Habit.id == habit_id, Habit.user_id == user_id))
        )
        habit = habit_result.scalar_one_or_none()
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
            )

        # Get all entries
        all_entries_result = await self.db.execute(
            select(HabitEntry).where(HabitEntry.habit_id == habit_id)
        )
        all_entries = list(all_entries_result.scalars().all())

        # Get completed entries
        completed_entries_result = await self.db.execute(
            select(HabitEntry).where(
                and_(HabitEntry.habit_id == habit_id, HabitEntry.completed == True)
            )
        )
        completed_entries = list(completed_entries_result.scalars().all())

        total_completions = len(completed_entries)
        total_days_tracked = len(all_entries)
        completion_rate = (
            (total_completions / total_days_tracked * 100)
            if total_days_tracked > 0
            else 0.0
        )

        # Current month completions
        today = date.today()
        current_month_start = date(today.year, today.month, 1)
        current_month_completions = sum(
            1
            for entry in completed_entries
            if entry.entry_date >= current_month_start
        )

        # Current week completions
        current_week_start = today - timedelta(days=today.weekday())
        current_week_completions = sum(
            1
            for entry in completed_entries
            if entry.entry_date >= current_week_start
        )

        return CompletionStats(
            total_completions=total_completions,
            total_days_tracked=total_days_tracked,
            completion_rate=round(completion_rate, 2),
            current_month_completions=current_month_completions,
            current_week_completions=current_week_completions,
        )

    def _calculate_confidence_level(
        self, streak_info: StreakInfo, completion_stats: CompletionStats
    ) -> int:
        """Calculate confidence level based on streak and completion stats."""
        # Base confidence on current streak (50% weight)
        streak_score = min(streak_info.current_streak * 5, 50)

        # Completion rate contribution (40% weight)
        rate_score = completion_stats.completion_rate * 0.4

        # Bonus for active streak (10% weight)
        active_bonus = 10 if streak_info.is_active else 0

        total_score = streak_score + rate_score + active_bonus
        return min(int(total_score), 100)

    def _generate_motivational_message(
        self,
        habit_name: str,
        streak_info: StreakInfo,
        completion_stats: CompletionStats,
        confidence_level: int,
    ) -> str:
        """Generate personalized motivational message."""
        messages = []

        if streak_info.current_streak == 0:
            messages.append(
                f"Start your {habit_name} journey today! Every expert was once a beginner."
            )
        elif streak_info.current_streak < 7:
            messages.append(
                f"Great start! You're on a {streak_info.current_streak}-day streak with {habit_name}. Keep the momentum going!"
            )
        elif streak_info.current_streak < 30:
            messages.append(
                f"Impressive! {streak_info.current_streak} days strong! You're building a solid habit."
            )
        elif streak_info.current_streak < 100:
            messages.append(
                f"Outstanding! {streak_info.current_streak}-day streak! You're truly committed to {habit_name}."
            )
        else:
            messages.append(
                f"Legendary! {streak_info.current_streak} days of {habit_name}! You're an inspiration!"
            )

        if completion_stats.completion_rate >= 90:
            messages.append(
                f"With a {completion_stats.completion_rate:.1f}% completion rate, you're crushing it!"
            )
        elif completion_stats.completion_rate >= 70:
            messages.append("You're doing great! Stay consistent to reach even higher.")
        else:
            messages.append(
                "Every day is a new opportunity. You've got this!"
            )

        if streak_info.current_streak == streak_info.longest_streak and streak_info.current_streak > 0:
            messages.append("🔥 This is your longest streak yet!")

        return " ".join(messages)

    async def get_habit_analytics(
        self, habit_id: UUID, user_id: UUID
    ) -> HabitAnalytics:
        """Get comprehensive analytics for a habit."""
        # Get habit
        habit_result = await self.db.execute(
            select(Habit).where(and_(Habit.id == habit_id, Habit.user_id == user_id))
        )
        habit = habit_result.scalar_one_or_none()
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
            )

        # Get streak info and completion stats
        streak_info = await self.calculate_streak(habit_id, user_id)
        completion_stats = await self.get_completion_stats(habit_id, user_id)

        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(
            streak_info, completion_stats
        )

        # Generate motivational message
        motivational_message = self._generate_motivational_message(
            habit.name, streak_info, completion_stats, confidence_level
        )

        return HabitAnalytics(
            habit_id=habit_id,
            habit_name=habit.name,
            frequency=habit.frequency,
            streak_info=streak_info,
            completion_stats=completion_stats,
            confidence_level=confidence_level,
            motivational_message=motivational_message,
        )

    async def get_progress_trends(
        self,
        habit_id: UUID,
        user_id: UUID,
        days: int = 90,
    ) -> ProgressTrends:
        """Get progress trends over specified period."""
        # Verify habit ownership
        habit_result = await self.db.execute(
            select(Habit).where(and_(Habit.id == habit_id, Habit.user_id == user_id))
        )
        habit = habit_result.scalar_one_or_none()
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found"
            )

        # Get entries for the period
        start_date = date.today() - timedelta(days=days)
        entries_result = await self.db.execute(
            select(HabitEntry)
            .where(
                and_(
                    HabitEntry.habit_id == habit_id,
                    HabitEntry.entry_date >= start_date,
                )
            )
            .order_by(HabitEntry.entry_date.asc())
        )
        entries = list(entries_result.scalars().all())

        # Build daily data
        daily_data = []
        entries_by_date = {entry.entry_date: entry for entry in entries}
        
        current_date = start_date
        while current_date <= date.today():
            entry = entries_by_date.get(current_date)
            daily_data.append(
                DailyCompletionData(
                    date=current_date,
                    completed=entry.completed if entry else False,
                    mood=entry.mood if entry else None,
                    notes=entry.notes if entry else None,
                )
            )
            current_date += timedelta(days=1)

        # Calculate weekly summaries
        weekly_summaries = self._calculate_weekly_summaries(entries, habit, days)

        # Calculate monthly summaries
        monthly_summaries = self._calculate_monthly_summaries(entries, habit, days)

        # Determine overall trend
        overall_trend = self._determine_trend(entries, days)

        return ProgressTrends(
            daily_data=daily_data,
            weekly_summaries=weekly_summaries,
            monthly_summaries=monthly_summaries,
            overall_trend=overall_trend,
        )

    def _calculate_weekly_summaries(
        self, entries: List[HabitEntry], habit: Habit, days: int
    ) -> List[WeeklyProgress]:
        """Calculate weekly progress summaries."""
        weeks = {}
        for entry in entries:
            if entry.completed:
                week_start = entry.entry_date - timedelta(
                    days=entry.entry_date.weekday()
                )
                if week_start not in weeks:
                    weeks[week_start] = 0
                weeks[week_start] += 1

        summaries = []
        target_per_week = 7 if habit.frequency == "daily" else (habit.target_days or 3)

        for week_start in sorted(weeks.keys()):
            week_end = week_start + timedelta(days=6)
            completions = weeks[week_start]
            summaries.append(
                WeeklyProgress(
                    week_start=week_start,
                    week_end=week_end,
                    completions=completions,
                    target=target_per_week,
                    completion_rate=round(
                        (completions / target_per_week * 100), 2
                    ),
                )
            )

        return summaries

    def _calculate_monthly_summaries(
        self, entries: List[HabitEntry], habit: Habit, days: int
    ) -> List[MonthlyProgress]:
        """Calculate monthly progress summaries."""
        months = {}
        for entry in entries:
            if entry.completed:
                month_key = (entry.entry_date.year, entry.entry_date.month)
                if month_key not in months:
                    months[month_key] = 0
                months[month_key] += 1

        summaries = []
        for month_key in sorted(months.keys()):
            year, month = month_key
            days_in_month = calendar.monthrange(year, month)[1]
            target = days_in_month if habit.frequency == "daily" else (habit.target_days or 20)
            completions = months[month_key]
            
            summaries.append(
                MonthlyProgress(
                    month=month,
                    year=year,
                    completions=completions,
                    target=target,
                    completion_rate=round((completions / target * 100), 2),
                )
            )

        return summaries

    def _determine_trend(self, entries: List[HabitEntry], days: int) -> str:
        """Determine overall trend direction."""
        if not entries:
            return "no_data"

        # Compare first half vs second half completion rates
        mid_point = days // 2
        cutoff_date = date.today() - timedelta(days=mid_point)

        first_half = [e for e in entries if e.entry_date < cutoff_date and e.completed]
        second_half = [
            e for e in entries if e.entry_date >= cutoff_date and e.completed
        ]

        first_rate = len(first_half) / mid_point if mid_point > 0 else 0
        second_rate = len(second_half) / mid_point if mid_point > 0 else 0

        if second_rate > first_rate * 1.1:
            return "improving"
        elif second_rate < first_rate * 0.9:
            return "declining"
        else:
            return "stable"

    async def check_streak_recovery(
        self, habit_id: UUID, user_id: UUID, grace_days: int = 1
    ) -> StreakRecoveryInfo:
        """Check if a streak can be recovered."""
        streak_info = await self.calculate_streak(habit_id, user_id)

        if streak_info.is_active or not streak_info.last_completed_date:
            return StreakRecoveryInfo(
                can_recover=False,
                days_since_last_completion=0,
                recovery_deadline=None,
                grace_period_days=grace_days,
            )

        days_since = (date.today() - streak_info.last_completed_date).days
        can_recover = days_since <= grace_days + 1
        recovery_deadline = (
            streak_info.last_completed_date + timedelta(days=grace_days + 1)
            if can_recover
            else None
        )

        return StreakRecoveryInfo(
            can_recover=can_recover,
            days_since_last_completion=days_since,
            recovery_deadline=recovery_deadline,
            grace_period_days=grace_days,
        )

    async def get_user_insights(self, user_id: UUID) -> HabitInsights:
        """Get aggregated insights for all user's habits."""
        # Get all active habits
        habits_result = await self.db.execute(
            select(Habit).where(
                and_(Habit.user_id == user_id, Habit.is_active == True)
            )
        )
        habits = list(habits_result.scalars().all())

        if not habits:
            return HabitInsights(
                best_performing_habits=[],
                needs_attention=[],
                total_active_streaks=0,
                average_streak_length=0.0,
                overall_completion_rate=0.0,
                motivational_insights=[
                    "Start tracking your habits to unlock insights!"
                ],
            )

        # Calculate metrics for each habit
        habit_metrics = []
        for habit in habits:
            try:
                analytics = await self.get_habit_analytics(habit.id, user_id)
                habit_metrics.append((habit.name, analytics))
            except Exception:
                continue

        # Sort by completion rate
        sorted_by_rate = sorted(
            habit_metrics,
            key=lambda x: x[1].completion_stats.completion_rate,
            reverse=True,
        )

        best_performing = [h[0] for h in sorted_by_rate[:3] if h[1].completion_stats.completion_rate >= 70]
        needs_attention = [h[0] for h in sorted_by_rate[-3:] if h[1].completion_stats.completion_rate < 50]

        # Calculate aggregates
        active_streaks = sum(
            1 for _, a in habit_metrics if a.streak_info.is_active
        )
        avg_streak = (
            sum(a.streak_info.current_streak for _, a in habit_metrics)
            / len(habit_metrics)
            if habit_metrics
            else 0.0
        )
        overall_rate = (
            sum(a.completion_stats.completion_rate for _, a in habit_metrics)
            / len(habit_metrics)
            if habit_metrics
            else 0.0
        )

        # Generate insights
        insights = []
        if active_streaks > 0:
            insights.append(
                f"🔥 You have {active_streaks} active streak{'s' if active_streaks != 1 else ''}! Keep the momentum going!"
            )
        if overall_rate >= 80:
            insights.append(
                "⭐ Outstanding performance! You're maintaining excellent consistency."
            )
        elif overall_rate >= 60:
            insights.append(
                "💪 Good job! You're building strong habits. Keep pushing!"
            )
        else:
            insights.append(
                "🌱 Every journey starts with small steps. Focus on consistency!"
            )

        if best_performing:
            insights.append(
                f"✨ Your top habits: {', '.join(best_performing[:2])}"
            )

        return HabitInsights(
            best_performing_habits=best_performing,
            needs_attention=needs_attention,
            total_active_streaks=active_streaks,
            average_streak_length=round(avg_streak, 1),
            overall_completion_rate=round(overall_rate, 2),
            motivational_insights=insights,
        )
