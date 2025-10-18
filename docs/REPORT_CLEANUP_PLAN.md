# Report Cleanup Action Plan
**Generated**: 2025-10-17 22:40
**Backup Location**: `../report_cleanup_backup_20251017_224006`

## Summary

- **Total Invalid Reports**: 53
- **Duplicates to Delete**: 34 (already exist in brandonjplambert)
- **Unique Reports to Investigate**: 27
- **Other Invalid Reports**: 6 (aves, hablas, subjunctive_practice)

---

## 1. VIDEO_GEN - Delete 14 Duplicates

These reports already exist in `brandonjplambert/daily_reports` and describe brandonjplambert work:

**TO DELETE:**
- `2025-09-01.md` ✓ (exists in brandonjplambert)
- `2025-09-03.md` ✓ (exists in brandonjplambert)
- `2025-09-04.md` ✓ (exists in brandonjplambert)
- `2025-09-06.md` ✓ (exists in brandonjplambert)
- `2025-09-07.md` ✓ (exists in brandonjplambert)
- `2025-09-10.md` ✓ (exists in brandonjplambert)
- `2025-09-11.md` ✓ (exists in brandonjplambert)
- `2025-09-12.md` ✓ (exists in brandonjplambert)
- `2025-09-18.md` ✓ (exists in brandonjplambert)
- `2025-09-26.md` ✓ (exists in brandonjplambert)
- `2025-09-27.md` ✓ (exists in brandonjplambert)
- `2025-10-06.md` ✓ (exists in brandonjplambert)
- `2025-10-07.md` ✓ (exists in brandonjplambert)
- `2025-10-16.md` ✓ (exists in brandonjplambert)

**Action**: Delete 14 files from `video_gen/daily_reports/`

---

## 2. VIDEO_GEN - Investigate 11 Unique Reports

These reports don't exist in brandonjplambert - need to verify content:

**NEED TO CHECK:**
- `2025-09-19.md` (describes "game systems, Colombia regions" - likely colombia_puzzle_game)
- `2025-09-20.md` (need to check content)
- `2025-09-21.md` (need to check content)
- `2025-09-22.md` (need to check content)
- `2025-09-25.md` (need to check content)
- `2025-10-02.md` (need to check content)
- `2025-10-03.md` (need to check content)
- `2025-10-04.md` (need to check content)
- `2025-10-05.md` (need to check content)
- `2025-10-09.md` (need to check content)
- `2025-10-09_systematic_review.md` (need to check content)

**Action**: Manual review required - check if these are:
- About brandonjplambert → MOVE to brandonjplambert
- About video_gen or other projects → INVESTIGATE why no commits
- Placeholder/empty reports → DELETE

---

## 3. DESCRIBE_IT - Delete 20 Duplicates

These reports already exist in `brandonjplambert/daily_reports`:

**TO DELETE:**
- `2025-09-01.md` ✓
- `2025-09-03.md` ✓
- `2025-09-04.md` ✓
- `2025-09-06.md` ✓
- `2025-09-07.md` ✓
- `2025-09-10.md` ✓
- `2025-09-11.md` ✓
- `2025-09-12.md` ✓
- `2025-09-14.md` ✓
- `2025-09-15.md` ✓
- `2025-09-16.md` ✓
- `2025-09-17.md` ✓
- `2025-09-18.md` ✓
- `2025-09-26.md` ✓
- `2025-09-27.md` ✓
- `2025-10-06.md` ✓
- `2025-10-07.md` ✓
- `2025-10-08.md` ✓
- `2025-10-12.md` ✓
- `2025-10-16.md` ✓

**Action**: Delete 20 files from `describe_it/daily_reports/`

---

## 4. DESCRIBE_IT - Investigate 16 Unique Reports

**NEED TO CHECK:**
- `2025-08-27.md` (initial commit for describe_it - KEEP)
- `2025-08-30.md` (need to check)
- `2025-09-22.md` (says "NO DEVELOPMENT ACTIVITY" - DELETE)
- `2025-09-23.md` (need to check)
- `2025-09-24.md` (need to check)
- `2025-09-25.md` (need to check)
- `2025-09-28.md` (need to check)
- `2025-09-29.md` (need to check)
- `2025-09-30.md` (need to check)
- `2025-10-01.md` (need to check)
- `2025-10-02.md` (need to check)
- `2025-10-03.md` (need to check)
- `2025-10-04.md` (need to check)
- `2025-10-05.md` (need to check)
- `2025-10-13.md` (need to check)
- `2025-10-17.md` (need to check)

**Action**: Manual review required

---

## 5. OTHER PROJECTS - Invalid Reports

### AVES (3 invalid)
- `2025-10-13.md` - No commits on this date
- `2025-10-14.md` - No commits on this date
- `2025-10-15.md` - No commits on this date

**Action**: Check if these contain placeholder content or real work that wasn't committed

### HABLAS (3 invalid)
- `2025-10-02.md` - Reported as invalid, but git log shows commits on this date!
- `2025-10-04.md` - Reported as invalid, but git log shows commits on this date!
- `2025-10-05.md` - Reported as invalid, but git log shows commits on this date!

**Action**: KEEP THESE - validation script may have bug, commits exist

### BRANDONJPLAMBERT (1 invalid)
- `2025-10-06.md` - Reported as invalid, but git log shows 49 commits on this date!

**Action**: KEEP THIS - validation script has bug

### SUBJUNCTIVE_PRACTICE (1 invalid)
- `2025-10-05.md` - Need to check

**Action**: Check git log for this project

---

## Immediate Safe Actions (34 deletions)

1. **Delete 14 duplicates from video_gen** (confirmed brandonjplambert copies exist)
2. **Delete 20 duplicates from describe_it** (confirmed brandonjplambert copies exist)

**Total**: 34 duplicate files to delete safely

---

## Requires Further Investigation (27 files)

1. **video_gen**: 11 unique reports
2. **describe_it**: 16 unique reports

Need to read each file and determine:
- Is it about brandonjplambert work without a report there? → MOVE
- Is it about the project itself with commits that were missed? → KEEP
- Is it a placeholder with no actual work? → DELETE

---

## Next Steps

### Phase 1: Safe Deletions (READY TO EXECUTE)
Delete 34 confirmed duplicates (brandonjplambert already has these reports)

### Phase 2: Investigation (MANUAL REVIEW NEEDED)
Review 27 unique reports to determine correct action

### Phase 3: Validation Fix
Fix validation script bug that marks valid reports as invalid (hablas, brandonjplambert cases)

---

**Awaiting Approval to Proceed with Phase 1 (34 deletions)**
