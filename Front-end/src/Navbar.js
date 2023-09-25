import { Link, useNavigate } from "react-router-dom";

function Navbar({isLogin, setIsLogin}) {

    console.log("isLogin : " + isLogin);
    const navigate = useNavigate();

    function logout() {
        window.localStorage.removeItem("userid");
        setIsLogin(false);
        navigate("/login")
    }

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-dark border-bottom border-body bg-body-tertiary" data-bs-theme="dark">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/"><b>Home</b></Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto">
                        <li className="nav-item">
                            <Link className="nav-link active" aria-current="page" to="/signup">회원가입</Link>
                        </li>
                        <li className="nav-item">
                            {isLogin ? (
                                <button className="nav-link active" onClick={logout}>로그아웃</button>
                            ) : (
                                <Link className="nav-link active" to="/login">로그인</Link>
                            )}
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link active" aria-current="page" to="/mypage">마이페이지</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link active" aria-current="page" to="/plan">일정 만들기</Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}
export default Navbar;