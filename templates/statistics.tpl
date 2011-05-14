<!-- Statistics -->
%from functions import *

%if rq.q.has_key('fb_user_id'):
    %user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
    %statistics = get_statistics(user)
%end

%if rq.q.has_key('round_id'):
    %r = get_round(round_id = int(rq.q.getfirst('round_id')))
%end

<div id="statistics" class="statistics">
    %if not rq.q.has_key('round_id'):
    <h3>إحصائياتك</h3>

    <table>
        <tr>
            <td>عدد الجولات:</td>
            <td><span>{{statistics.rounds_num}}</span></td>
        </tr>
        <tr>
            <td>عدد الأسئلة:</td>
            <td><span>{{statistics.questions_num}}</span></td>
        </tr>
        <tr>
            <td>الإجابات الصحيحة:</td>
            <td><span>{{statistics.correct_answers}}</span></td>
        </tr>
        <tr>
            <td>الإجابات الخاطئة:</td>
            <td><span>{{statistics.wrong_answers}}</span></td>
        </tr>
        <tr>
            <td>النقاط الأساسية:</td>
            <td><span>{{statistics.points}}</span></td>
        </tr>
        <tr>
            <td>النقاظ الإضافية:</td>
            <td><span>{{statistics.extra_points}}</span></td>
        </tr>
        <tr>
            <td>إجمالي النقاط:</td>
            <td><span>{{statistics.total_points}}</span></td>
        </tr>
    </table>
    
    %elif rq.q.has_key('round_id'):
    
    <h3>إحصائيات الجولة</h3>
    
    <table>
        <tr>
            <td>عدد الأسئلة:</td>
            <td><span id="question_num">{{r.question_num}}</span></td>
        </tr>
        <tr>
            <td>الإجابات الصحيحة:</td>
            <td><span id="correct_answers">{{r.correct_answers}}</span></td>
        </tr>
        <tr>
            <td>الإجابات الخاطئة:</td>
            <td><span id="wrong_answers">{{r.wrong_answers}}</span></td>
        </tr>
        <tr>
            <td>النقاط:</td>
            <td><span id="points">{{r.points}}</span></td>
        </tr>
    </table>
    %end
</div>
