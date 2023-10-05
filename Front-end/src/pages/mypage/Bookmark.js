import React from "react";
import styled from "styled-components";
import TouristSpot from '../components/TouristSpot';
import Sidebar from '../components/Sidebar';

const PageContainer = styled.div`
  display: flex;
`;

const Container = styled.div`
  display: flex;
  flex-wrap: wrap;
//   justify-content: space-between;
  justify-content: left;
  padding: 20px;
`;

const TextContainer = styled.div`
  width: 100%; /* 컨테이너 전체 너비를 사용하도록 설정 */
`;

const Text = styled.h2`
  font-size: 20px;
  font-weight: lighter;
  margin-bottom: 20px;
`;

const Bookmark = () => {
//   // 북마크된 관광지 데이터 (예시)
//   const [bookmarkedTouristSpots, setBookmarkedTouristSpots] = useState([
    // 북마크된 관광지 데이터 (예시)
  const bookmarkedTouristSpots = [
    {
      id: 1,
      name: "쇠소깍",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150831_76%2F1441025139566jlxeJ_JPEG%2F126362588156648_0.jpg",
      tags: ["관광지","자연"],
    },
    {
      id: 2,
      name: "용머리해안",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150901_66%2F14410456277055t8yW_JPEG%2F13491455_0.jpg",
      tags: ["관광지"],
    },
    {
      id: 3,
      name: "스누피가든",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20230111_200%2F16734217449280D9xr_JPEG%2F%25B3%25D7%25C0%25CC%25B9%25F6_%25BA%25EA%25B7%25A3%25B5%25E5%25B0%25CB%25BB%25F6_%25B8%25DE%25C0%25CE%25BD%25E6%25B3%25D7%25C0%25CF_PC_488x470_10Mb.jpg",
      tags: ["관광지"],
    },
    {
      id: 4,
      name: "9.81파크 제주",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fnaverbooking-phinf.pstatic.net%2F20230719_182%2F1689732791017ByNh1_PNG%2F20203_%25B7%25B9%25C0%25CC%25BD%25CC_%25C6%25C4%25B6%25F5%25C7%25CF%25B4%25C3.png",
      tags: ["관광지"],
    },
    {
      id: 5,
      name: "대포주상절리",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fvideo-phinf.pstatic.net%2F20230815_8%2F1692083439344JhO5h_JPEG%2Fd62bcacf-3b3a-11ee-ba0a-48df379cc9e4_03.jpg",
      tags: ["관광지"],
    },
    {
      id: 6,
      name: "천제연폭포",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150831_207%2F1440992289833tONYr_JPEG%2F11491637_0.jpg",
      tags: ["관광지"],
    },
    {
      id: 7,
      name: "휴애리자연생활공원",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20230904_295%2F1693806066265OCuAl_JPEG%2FKakaoTalk_20230904_143904995_01.jpg",
      tags: ["관광지"],
    },
    {
      id: 8,
      name: "도두동무지개해안도로",
      image: "https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20200325_229%2F1585100287523Q6sGV_JPEG%2FUb-_866t13IS6lzjvWhgT8Gx.jpg",
      tags: ["관광지"],
    },
    // 다른 북마크된 관광지 추가
//   ]);
  ];

//    // 북마크 추가 및 삭제 함수
//    const toggleBookmark = (id) => {
//     const updatedBookmarkedSpots = bookmarkedTouristSpots.map((spot) => {
//       if (spot.id === id) {
//         // 클릭한 아이템의 북마크 상태를 반전
//         return { ...spot, isBookmarked: !spot.isBookmarked };
//       }
//       return spot;
//     });

//     setBookmarkedTouristSpots(updatedBookmarkedSpots);
//   };

//   // 북마크된 데이터만 필터링
//   const filteredBookmarkedSpots = bookmarkedTouristSpots.filter(
//     (spot) => spot.isBookmarked
//   );

  return (
    <PageContainer>
      <Sidebar /> {/* 사이드바를 여기에 추가 */}
      <Container>
        <TextContainer>
          <Text>나의 찜한 장소</Text>
        </TextContainer>
        {bookmarkedTouristSpots.map((spot) => (
            <TouristSpot
            key={spot.id}
            name={spot.name}
            description={spot.description}
            imageUrl={spot.image}
            location="" // 이 부분은 필요에 따라 수정
            tags={spot.tags}
            rating={spot.rating}
            />
        ))}
      </Container>
    </PageContainer>
  );
};

export default Bookmark;
