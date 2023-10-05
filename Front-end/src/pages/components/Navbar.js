import React from "react";
import { Link } from "react-router-dom";
import "../components/Navbar.css"; // 스타일링을 위한 CSS 파일을 임포트합니다.

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img
          src="https://i.namu.wiki/i/dkzcvnkxu1u9nrgRSAPK0v4G1z3Vb-pjIqw51cV8ZllmrsuDLPaF37VEl3a01mXtkapBFTeR7pdpeoXQ5sLAhiW9Zqzizlzd9rXmKEUiVD7LKmZOVqE0SWo-eznehgbhpgdpEQ4wv1xP3QpJbom4UA.svg"
          alt="아이콘 또는 이미지"
          className="icon" // 이미지 스타일링을 위한 클래스 추가
        />
      </div>
      <div className="navbar-right">
        <ul>
          <li>
            <Link to="/">메인</Link>
          </li>
          <li>
            <Link to="/my-page">마이페이지</Link>
          </li>
          <li>
            <Link to="/bookmark-page">북마크</Link>
          </li>
          <li>
            <Link to="/record-page">여행기록</Link>
          </li>
          {/* 다른 네비게이션 항목 추가 */}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
