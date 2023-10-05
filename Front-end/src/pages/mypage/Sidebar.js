import React from "react";
import styled from "styled-components";

const SidebarContainer = styled.div`
  width: 600px; /* 원하는 사이드바 너비 설정 */
  background-color: #f0f0f0; /* 사이드바 배경색 설정 */
  padding: 20px;
`;

const Sidebar = () => {
  return (
    <SidebarContainer>
      {/* 여기에 사이드바 내용을 추가합니다. */}
      <h2>Sidebar</h2>
      {/* 추가적인 링크나 메뉴 아이템을 추가할 수 있습니다. */}
    </SidebarContainer>
  );
};

export default Sidebar;