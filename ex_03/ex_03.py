import logging

logging.basicConfig(
    level=logging.INFO,
    filename="tournament_app.log",
    filemode="a",
    format="[%(asctime)s] - [%(levelname)s] - %(message)s"
)

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]


# CHỨC NĂNG 1: Hiển thị danh sách trận đấu
def display_matches(match_list):
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<8} | Trạng thái")
    print("-" * 70)

    try:
        for match in match_list:
            score = f"{match['score_a']}-{match['score_b']}"
            print(f"{match['match_id']:<10} | {match['team_a']:<15} | {match['team_b']:<15} | {score:<8} | {match['status']}")

    except KeyError as error:
        logging.error(f"Missing key while displaying matches: {error}")

    logging.info("User viewed the match list.")


# CHỨC NĂNG 2: Thêm trận đấu mới
def add_match(match_list):
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")

    while True:
        match_id = input("Nhập mã trận đấu: ").strip().upper()

        if not match_id:
            print("Mã trận đấu không được để trống.")
            logging.warning(
                "User tried to add a match with empty match ID."
            )
        else:
            break

    for match in match_list:
        if match["match_id"] == match_id:
            print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại.")
            logging.warning(
                f"Match ID {match_id} already exists."
            )
            return

    while True:
        team_a = input("Nhập tên Đội A: ").strip()

        if not team_a:
            print("Tên đội không được để trống.")
            logging.warning(
                "User tried to add a match with empty team name."
            )
        else:
            break

    while True:
        team_b = input("Nhập tên Đội B: ").strip()

        if not team_b:
            print("Tên đội không được để trống.")
            logging.warning(
                "User tried to add a match with empty team name."
            )
        else:
            break

    new_match = {
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }

    match_list.append(new_match)

    print(f"Thành công: Đã thêm trận đấu {match_id}.")
    logging.info(
        f"Match {match_id} added successfully"
    )


# CHỨC NĂNG 3: Cập nhật tỷ số
def update_score(match_list):
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")

    while True:
        match_id = input(
            "Nhập mã trận đấu cần cập nhật: "
        ).strip().upper()

        if not match_id:
            print("Mã trận đấu không được để trống.")
        else:
            break

    for match in match_list:

        if match["match_id"] == match_id:

            print(
                f"\nTrận đấu: "
                f"{match['team_a']} vs {match['team_b']} "
                f"({match['status']})"
            )

            while True:
                try:
                    score_a = int(input("Nhập điểm Đội A: "))

                    if score_a < 0:
                        print("Điểm số phải lớn hơn hoặc bằng 0.")
                        logging.error(f"Negative score input detected: {score_a}")
                    else:
                        break

                except ValueError as error:
                    print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
                    logging.error(f"Invalid score input. Error: {error}")

            while True:
                try:
                    score_b = int(input("Nhập điểm Đội B: "))
                    if score_b < 0:
                        print("Điểm số phải lớn hơn hoặc bằng 0.")
                        logging.error(f"Negative score input detected: {score_b}")
                    else:
                        break

                except ValueError as error:
                    print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
                    logging.error(f"Invalid score input. Error: {error}")

            match["score_a"] = score_a
            match["score_b"] = score_b

            if score_a == 0 and score_b == 0:

                confirm = input("Tỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()

                if confirm == "y":
                    match["status"] = "Completed"
                else:
                    match["status"] = "Pending"

            else:
                match["status"] = "Completed"

            print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
            logging.info(f"Match {match_id} score updated successfully")
            return

    else:
        print(f"Không tìm thấy trận đấu mang mã {match_id}.")
        logging.warning(f"User tried to update non-existing match {match_id}")


# HÀM PHỤ: Xác định đội thắng
def determine_winner(match):
    if match["status"] == "Pending":
        return "Not Started"

    if match["score_a"] > match["score_b"]:
        return match["team_a"]

    if match["score_b"] > match["score_a"]:
        return match["team_b"]

    return "Draw"


# CHỨC NĂNG 4: Báo cáo
def generate_report(match_list):
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")

    completed_count = 0

    try:
        for match in match_list:
            if match["status"] == "Completed":
                winner = determine_winner(match)
                print(
                    f"{match['match_id']}: "
                    f"{match['team_a']} "
                    f"{match['score_a']}-"
                    f"{match['score_b']} "
                    f"{match['team_b']} "
                    f"| Kết quả: {winner}"
                )
                completed_count += 1

    except KeyError as error:
        logging.error(f"Missing key while generating report: {error}")

    if completed_count == 0:
        print("Chưa có trận đấu nào hoàn thành.")

    print(f"\nTổng số trận đã hoàn thành: {completed_count}")
    logging.info("User generated tournament report.")


# MAIN
def main():
    choice = ""
    while choice != "5":
        print()
        print("===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. Cập nhật tỷ số trận đấu")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("==================================================")

        choice = input("Chọn chức năng (1-5): ")
        match choice:
            case "1":
                display_matches(matches)
            case "2":
                add_match(matches)
            case "3":
                update_score(matches)
            case "4":
                generate_report(matches)
            case "5":
                print("Cảm ơn bạn đã sử dụng hệ thống.")
                logging.info("Tournament management system closed.")
            case _:
                print("Lựa chọn không hợp lệ!")
                logging.warning("Invalid menu choice selected")
main()