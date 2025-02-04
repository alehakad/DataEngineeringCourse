-- Are any of the student's characteristics (from studentInfo)
-- good predictors to their academic achievements?

-- find column with max correlation with average mark of student 


-- 1) calculate weighted average mark over all subjects per student (assuming that 100 is total weigth for each course)
with student_avg_scores as (
	select 
		id_student,
		avg(weight*score/100) as avg_score 
	from studentAssessment t1 join
	assessments t2 on
	t1.id_assessment = t2.id_assesment
	group by id_student
),
student_info_ext as (
select 
	(case 
		when age_band = '0-35' then 1
		when age_band = '35-55' then 2
		when age_band = '55<=' then 3
		else NULL end
	) as age_band_num,
    (case when gender='M' then 1 else -1 end) as gender_num,
    (case 
		when highest_education = 'HE Qualification' then 1
		when highest_education = 'Lower Than A Level' then 2
		when highest_education = 'A Level or Equivalent' then 3
		when highest_education = 'Post Graduate Qualification' then 4
		when highest_education = 'No Formal quals' then 5
        else NULL 
        end
	) as he_num,
    sa.avg_score 
from student_avg_scores sa join 
studentInfo si on 
sa.id_student = si.id_student
)
select 
    SUM((avg_score - (SELECT AVG(avg_score) FROM student_info_ext)) * 
        (gender_num - (SELECT AVG(gender_num) FROM student_info_ext))) / 
    (SQRT(SUM(POW(avg_score - (SELECT AVG(avg_score) FROM student_info_ext), 2))) * 
     SQRT(SUM(POW(gender_num - (SELECT AVG(gender_num) FROM student_info_ext), 2)))) AS corr,
     'gender' as prop
from student_info_ext
union
select 
    SUM((avg_score - (SELECT AVG(avg_score) FROM student_info_ext)) * 
        (age_band_num - (SELECT AVG(age_band_num) FROM student_info_ext))) / 
    (SQRT(SUM(POW(avg_score - (SELECT AVG(avg_score) FROM student_info_ext), 2))) * 
     SQRT(SUM(POW(age_band_num - (SELECT AVG(age_band_num) FROM student_info_ext), 2)))) AS corr,
     'age' as prop
from student_info_ext
union
select 
    SUM((avg_score - (SELECT AVG(avg_score) FROM student_info_ext)) * 
        (he_num - (SELECT AVG(he_num) FROM student_info_ext))) / 
    (SQRT(SUM(POW(avg_score - (SELECT AVG(avg_score) FROM student_info_ext), 2))) * 
     SQRT(SUM(POW(he_num - (SELECT AVG(he_num) FROM student_info_ext), 2)))) AS corr,
     'education' as prop
from student_info_ext;




