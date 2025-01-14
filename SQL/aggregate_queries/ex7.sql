-- Do students tend to get higher or lower grades over the course of their studies --

-- 1) Find absolute dates of assessments per student per course --
WITH student_time_marks AS (
    SELECT 
        id_student,
        code_module,
        code_presentation,
        id_assessment,
        score,
        DATE_ADD(
            CASE 
                WHEN SUBSTRING(code_presentation, 5, 1) = 'B' THEN CONCAT(SUBSTRING(code_presentation, 1, 4), '-02-01')
                WHEN SUBSTRING(code_presentation, 5, 1) = 'J' THEN CONCAT(SUBSTRING(code_presentation, 1, 4), '-10-01')
            END, 
            INTERVAL date_submitted DAY
        ) AS submission_date
    FROM studentAssessment sa
    JOIN assessments asm
    ON sa.id_assessment = asm.id_assesment
),
-- 2) Calculate running weighted average per student over date --
running_average_marks AS (
    SELECT 
        id_student, 
        submission_date,
        AVG(score) OVER (PARTITION BY id_student ORDER BY submission_date) AS running_avg
    FROM student_time_marks
),
first_last_average AS (
    SELECT 
        DISTINCT(id_student),
        FIRST_VALUE(running_avg) OVER (PARTITION BY id_student ORDER BY submission_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_avg,
        LAST_VALUE(running_avg) OVER (PARTITION BY id_student ORDER BY submission_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_avg
    FROM running_average_marks
)
SELECT 
    CASE 
        WHEN last_avg > first_avg THEN 'increase' 
        WHEN last_avg < first_avg THEN 'decrease' 
        ELSE 'no_change' 
    END AS avg_change,
    COUNT(*) AS student_count
FROM first_last_average
GROUP BY avg_change;
