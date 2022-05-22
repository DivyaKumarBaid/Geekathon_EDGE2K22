import React, { useState, useEffect, useRef } from "react";
import { FaStethoscope as Appointments } from "react-icons/fa";
import { AiFillStar as Star } from "react-icons/ai";
import { BiComment as Review } from "react-icons/bi";
import { FiFilter as Filter } from "react-icons/fi";
import FakeData from "./Data";
import "./Home.css";

const Home = () => {
    return (
        <>
            <SearchSection />
        </>
    );
}

const SearchSection = () => {
    const [Loading, setLoading] = useState(true);
    const [Data, setData] = useState([]);
    const name = useRef(null);
    const specialist = useRef(null);

    const FetchData = () => {
        // Fetching Data
        console.log(FakeData);
        setData(FakeData);
        setLoading(false);
    }

    useEffect(() => {
        FetchData();
    },[])

    return (
        <>
        <SearchBar name={name} specialist={specialist}/>
        <SearchResults data={Data} loading={Loading}/>
        </>
    );
}

const SearchBar = (props) => {
    const [filter, setfilter] = useState(false);
    return (
        <div className="search-section">
            <div className="search-top">
                <input type="text" placeHolder="name" ref={props.name}/>
                <div className="search-filter">
                    <Filter color={`${filter ? "#10ac79" : "rgb(219, 219, 219)"}`} 
                        onClick={(e) => {setfilter(!filter)}}
                        cursor="pointer"
                        size="1.7em"
                    />
                    <div className="search-btn">Search</div>
                </div>
            </div>
            { filter ? (
                <div className="search-filter">
                    <input type="text" placeHolder="specialist" className="Specialist" ref={props.specialist}/>
                </div>
            ) : null }
        </div>
    );
};

const SearchResults = (props) => {
    const [mapIndex, setMapIndex] = useState(0);
    console.log(props.data[mapIndex], mapIndex);
    return (
        <div className="viewer">
            <div className="data-viewer">
                {props.data.map((data, index) => {
                    console.log(index);
                    return <DocCard data={data} Active={setMapIndex} key={index} index={index}/>
                })}
            </div>
            {props.data[mapIndex]!==undefined ?
                <div className="google-map">
                    <iframe src={props.data[mapIndex].map_link} width="600" height="450" allowfullscreen="" title="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </div> : null
            }
        </div>
    );
};

const DocCard = (props) => {
    const { data } = props;
    console.log(props.index);
    return (
        <div className="doc-card" onClick={(e) => {props.Active(props.index)}}>
            <div className="doc-card-name">{"Dr. " + data.doc}</div>
            <div className="doc-card-specialist_in">{data.specialist_in}</div>
            <div className="doc-card-stats">
                <div className="doc-card-rating">
                    <p>{data.rating_avg}</p>
                    <Star/>
                </div>
                <div className="doc-card-appointments">
                    <p>{data.appointment_count}</p>
                    <Appointments/>
                </div>
                <div className="doc-card-review">
                    <p>{data.reviews.length}</p>
                    <Review/>
                </div>
            </div>
        </div>
    );
};

export default Home;