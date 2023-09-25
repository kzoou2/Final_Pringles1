import axios from "axios";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function QNA() {
    const [questionList, setQuestionList] = useState([]);

    useEffect(() => {
        async function getQuestionList() {
            try {
                const result = await axios.get("http://localhost:8080/mypage/qna");
                setQuestionList(result.data);
            } catch(error) {
                console.log(error);
            }
        }
        getQuestionList();
    }, [])

    return (
        <div>
            질의응답 작성 페이지
            <table className="table text-center my-3">
                <thead className="table-dark">
                    <tr>
                        <th>No</th>
                        <th>제목</th>
                        <th>작성시간</th>
                    </tr>
                </thead>
                <tbody>
                    {questionList.map((question, index) => {
                        return (
                            <tr key={index}>
                                <td>{index+1}</td>
                                <td>
                                    <Link to={`/mypage/qna/${question.id}`}>{question.subject}</Link>
                                </td>
                                <td>{question.createDate}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}

export default QNA;