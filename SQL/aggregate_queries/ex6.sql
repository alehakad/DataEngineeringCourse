-- correlation between course assessments and exam results -- 
-- 1) find all exam marks per student per course --
WITH exam_marks AS (
    SELECT id_student, code_module, code_presentation, score AS exam_score
    FROM assessments asm
    JOIN studentAssessment sa ON asm.id_assesment = sa.id_assessment
    WHERE asm.assessment_type = 'Exam'
),
-- 2) find weighted average assignements marks per student per course --
avg_assignments_marks AS (
    SELECT id_student, code_module, code_presentation, SUM(score * weight)/SUM(weight) AS avg_score
    FROM assessments asm
    JOIN studentAssessment sa ON asm.id_assesment = sa.id_assessment
    WHERE asm.assessment_type != 'Exam'
    GROUP BY id_student, code_module, code_presentation
),
-- 3) select only students that did exam and assignements --
combined_data AS (
    SELECT 
        em.id_student,
        em.code_module,
        em.code_presentation,
        em.exam_score,
        am.avg_score
    FROM exam_marks em
    JOIN avg_assignments_marks am
    USING (id_student, code_module, code_presentation)
),
-- 4) find correlation --
stats AS (
    SELECT
        AVG(exam_score) AS mean_exam,
        AVG(avg_score) AS mean_avg,
        STDDEV(exam_score) AS stddev_exam,
        STDDEV(avg_score) AS stddev_avg
    FROM combined_data
),
covariance AS (
    SELECT
        SUM((exam_score - (SELECT mean_exam FROM stats)) *
            (avg_score - (SELECT mean_avg FROM stats))) / 
        COUNT(*) AS cov_xy
    FROM combined_data
)
SELECT 
	cov_xy / (stddev_exam * stddev_avg) AS correlation
FROM covariance, stats;