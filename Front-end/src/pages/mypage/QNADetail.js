import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

function QNADetail() {
    const [question, setQuestion] = useState([]);
    const [answer, setAnswer] = useState([]);
    const [answerText, setAnswerText] = useState([]);
    const params = useParams();
    const navigate = useNavigate();
    
    useEffect(() => {
        async function getQuestion() {
            try {
                const result = await axios.get(`http://localhost:8080/mypage/qna/${params.id}`)
                console.log(result);
                setQuestion(result.data);
                setAnswer(result.data.answerlist);
            } catch (error) {
                console.log(error);
            }
        }
        getQuestion();
    }, [params.id])

    function onChange(e) {
       setAnswerText(e.target.value) 
    }

    async function onSubmit(e) {
        if (answerText === "") {
            alert("답변 내용은 필수 입력사항입니다.")
        } else {
            e.preventDefault();
            try {
                const result = await axios.post(`http://localhost:8080/answer-create/${params.id}`, {
                    content: answerText,
                });
                if (result.status === 200) {
                    navigate(0);
                }
            } catch (error) {
                console.log(error);
            }
        }
    }

    return (
        <div>
            <h2 className="border-bottom py-2">{question.subject}</h2>
            <div className="card my-3">
                <div className="card-body">
                    <div className="card-text" style={{whiteSpace: 'pre-line'}}>{question.content}</div>
                    <div className="d-flex justify-content-end">
                        <div className="badge bg-light text-dark p-2 text-start">
                            <div>작성: {question.createDate}</div>
                        </div>
                    </div>
                </div>
            </div>
            <h5 className="border-bottom py-2">{answer.length}개의 답변</h5>
            {answer.map((answer, index) => {
                return (
                    <div className="card my-3" key={index}>
                    <div className="card-body">
                        <div className="card-text" style={{whiteSpace: 'pre-line'}}>{answer.content}</div>
                        <div className="d-flex justify-content-end">
                            <div className="badge bg-light text-dark p-2 text-start">
                                <div>작성: {answer.createDate}</div>
                            </div>
                        </div>
                    </div>
                </div>
                )
            })}
                        
            <form onSubmit={onSubmit} className="my-3">
                <textarea 
                    onChange={onChange} value={answerText} 
                    name="content" id="content" rows="10" className="form-control"></textarea>
                <input type="submit" value="답변등록" className="btn btn-primary my-2"></input>
            </form>
        </div>
)
}

export default QNADetail;