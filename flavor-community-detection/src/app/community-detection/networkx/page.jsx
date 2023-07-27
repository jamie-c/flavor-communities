import WallPaper from '@/components/Wallpaper';
import { Chip, Stack, Typography } from '@mui/material';

const NetworkXResult = async () => {
    let jsonData = {};

    try {
        const response = await fetch('http://localhost:3000/api/networkx');
        jsonData = await response.json();

    } catch (error) {
        console.error('Error fetching Python result:', error);
        jsonData = { error: 'Failed to fetch Python result' };
    }

    const { name, method, time_elapsed } = jsonData;

    return (
        <Stack 
            flexDirection='column'
            justifyContent='center'
            alignItems='center'
            className='min-w-screen min-h-screen'
        >
        <Stack 
            className='max-w-3xl z-10 bg-gray-200 bg-opacity-40 
                backdrop-filter backdrop-blur-lg shadow-md rounded-md p-4'
            direction='column' 
            spacing={1}
            >
            {jsonData.error && <Chip label={jsonData.error} color='error' />}
            <Typography>
                Ran {method} {name} community detection in {time_elapsed} milliseconds.
            </Typography>
            {Object.keys(jsonData).map((key) => (
                key.toLocaleLowerCase().includes('community') ? (
                    <Stack 
                    className='bg-gray-300 backdrop-filter backdrop-blur-lg 
                    bg-opacity-10 shadow-sm rounded-md p-4' 
                    key={key} direction='row' flexWrap='wrap' width='100%' 
                    spacing={1} useFlexGap
                    >
                    <Typography 
                        className='w-full capitalize font-bold'
                        >
                        {key.replace('_', ' ')}
                    </Typography>
                { jsonData[key].map((value) => (
                    <Chip key={value} label={value} color='secondary'/>
                    ))}
                </Stack>
                ) : null
                ))}
        </Stack>
        <WallPaper />
        </Stack>
    );
};

export default NetworkXResult;
