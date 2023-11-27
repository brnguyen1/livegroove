import { Link } from "react-router-dom";

export default function Header() {

    return (
    <div className="fixed top-0 start-0 z-50 flex justify-between w-full p-4 border-b border-gray-200 bg-gray-50 dark:bg-gray-700 dark:border-gray-600">
        <Link to={"/"}>
            <div className="flex items-center ml-4 mr-auto font-semibold italic">
                LiveGroove
            </div>
        </Link>
    </div>
    )
}