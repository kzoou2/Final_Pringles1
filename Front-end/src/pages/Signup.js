import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {

    // 초기값 세팅 - 아이디, 이름, 비밀번호, 이메일
    const [username, setUsername] = useState("");
    const [userid, setUserid] = useState("");
    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] = useState("");
    const [email, setEmail] = useState("");
    
    // // 오류메세지 상태 저장
    // const [usernameMessage, setUsernameMessage] = useState("");
    // const [useridMessage, setUseridMessage] = useState("");
    // const [passwordMessage, setPasswordMessage] = useState("");
    // const [passwordConfirmMessage, setPasswordConfirmMessage] = useState("");
    // const [emailMessage, setEmailMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState([]);
    const navigate = useNavigate();

    // // 유효성 검사
    // const [isUsername, setIsUsername] = useState(false);
    // const [isUserid, setIsUserid] = useState(false);
    // const [isPassword, setIsPassword] = useState(false);
    // const [isPasswordConfirm, setIsPasswordConfirm] = useState(false);
    // const [isEmail, setIsEmail] = useState(false);


    function onChange(event) {

        if(event.target.name === "username") {
            setUsername(event.target.value)
        } else if (event.target.name === "userid") {
            setUserid(event.target.value)
        } else if (event.target.name === "password") {
            setPassword(event.target.value)
        } else if (event.target.name === "passwordConfirm") {
            setPasswordConfirm(event.target.value)
        } else if (event.target.name === "email") {
            setEmail(event.target.value)
        }
    }

    // const onChangeId = (e) => {
    //     const currentId = e.target.value;
    //     setUserid(currentId);
    //     const idRegExp = /^[a-zA-Z0-9][4,12]$/;

    //     if (!idRegExp.test(currentId)) {
    //         setUseridMessage("4-12자리 대소문자 또는 숫자만 입력해주세요.")
    //         setIsUserid(false);
    //     } else {
    //         setUseridMessage("사용가능한 아이디 입니다.");
    //         setIsUserid(true);
    //     }
    // }

    // const onChangePwd = (e) => {
    //     const currentPassword = e.target.value;
    //     setPassword(currentPassword);
    //     const pwdRegExp = /^(?=.*[a-zA-Z])(?=.*[!@#$%^&*+=-])(?=.*[0-9]).{8,25}$/;

    //     if (!pwdRegExp.test(currentPassword)) {
    //         setPassword("숫자, 영문자, 특수문자 조합으로 8자리 이상 입력해주세요.")
    //         setIsPassword(false);
    //     } else {
    //         setPasswordMessage("안전한 비밀번호입니다.");
    //         setIsPassword(true);
    //     }
    // }

    // const onChangePwdConfirm = (e) => {
    //     const currentPasswordConfirm = e.target.value;
    //     setPasswordConfirm(currentPasswordConfirm);

    //     if (password !== currentPasswordConfirm) {
    //         setPasswordConfirmMessage("비밀번호가 일치하지 않습니다.")
    //         setIsPasswordConfirm(false);
    //     } else {
    //         setPasswordConfirmMessage("비밀번호가 일치합니다.");
    //         setIsPasswordConfirm(true);
    //     }
    // }

    // const onChangeEmail = (e) => {
    //     const currentEmail = e.target.value;
    //     setEmail(currentEmail);
    //     const emailRegExp = /^[A-Za-z0-9_]+[A-Za-z0-9]*[@]{1}[A-Za-z0-9]+[A-Za-z0-9]*[.]{1}[A-Za-z]{1,3}$/;

    //     if (!emailRegExp.test(currentEmail)) {
    //         setEmailMessage("이메일 형식이 올바르지 않습니다.")
    //         setIsEmail(false);
    //     } else {
    //         setEmailMessage("사용가능한 이메일입니다.");
    //         setIsPasswordConfirm(true);
    //     }
    // }



    async function onSubmit(event) {
        event.preventDefault();

        const newErrorMessages = [];
        if (username === "") {
            newErrorMessages.push("이름은 필수 입력 항목입니다.");
        }
        if (userid === "") {
            newErrorMessages.push("아이디는 필수 입력 항목입니다.");
        }
        if (password === "") {
            newErrorMessages.push("비밀번호는 필수 입력 항목입니다.");
        }
        if (passwordConfirm === "") {
            newErrorMessages.push("비밀번호 확인은 필수 입력 항목입니다.");
        }
        if (email === "") {
            newErrorMessages.push("이메일은 필수 입력 항목입니다.");
        }
        if (password !== passwordConfirm) {
            newErrorMessages.push("비밀번호가 일치하지 않습니다.");
        }


        setErrorMessage(newErrorMessages);

        if (newErrorMessages.length === 0) {
            try {
                const result = await axios.post("http://localhost:8080/signup", {
                    username: username,
                    userid: userid,
                    password: password,
                    passwordConfirm: passwordConfirm,
                    email: email
                })
                if (result.status === 200) {
                    navigate("/login")
                }
            } catch(error) {
                // console.log(error.response.data);
                if (error.response && error.response.data) {
                    // 서버에서 반환한 에러메세지 출력
                    // alert(error.response.data);
                    setErrorMessage([error.response.data]);
                    setUsername("")
                    setUserid("")
                    setPassword("")
                    setPasswordConfirm("")
                    setEmail("")
                } else {
                    console.log(error);
                }
            }
        }
    }

    return (
        <div className="container my-3">
            <div className="my-3 border-bottom">
                <h3><b>회원가입</b></h3>
            </div>
            <br/>
            <form onSubmit={onSubmit}>
                {errorMessage.length > 0 &&
                    (<div className="alert alert-danger" role="alert">
                        {errorMessage.map((message, index) => (<div key={index}>{message}</div>))}
                    </div>)
                }
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">이름</label>
                    <input onChange={onChange} value={username} type="text" className="form-control" id="username" name="username"></input>
                </div>
                <div className="mb-3">
                    <label htmlFor="userid" className="form-label">아이디</label>
                    <input onChange={onChange} value={userid} type="text" className="form-control" id="userid" name="userid"></input>
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">비밀번호</label>
                    <input onChange={onChange} value={password} type="password" className="form-control" id="password" name="password"></input>
                </div>
                <div className="mb-3">
                    <label htmlFor="passwordConfirm" className="form-label">비밀번호 확인</label>
                    <input onChange={onChange} value={passwordConfirm} type="password" className="form-control" id="passwordConfirm" name="passwordConfirm"></input>
                </div>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">이메일</label>
                    <input onChange={onChange} value={email} type="email" className="form-control" id="email" name="email"></input>
                </div>
                <button type="sumbit" className="btn btn-primary">회원가입</button>
            </form>
        </div>
    )
}


export default Signup;